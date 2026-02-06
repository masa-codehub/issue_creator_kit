# ruff: noqa: T201
import time
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from issue_creator_kit.domain.document import Document
from issue_creator_kit.domain.interfaces import (
    IFileSystemAdapter,
    IGitAdapter,
    IGitHubAdapter,
)
from issue_creator_kit.usecase.roadmap_sync import RoadmapSyncUseCase
from issue_creator_kit.usecase.workflow import WorkflowUseCase


class IssueCreationUseCase:
    """
    UseCase for detecting new tasks in the virtual queue and creating GitHub Issues.
    """

    def __init__(
        self,
        fs_adapter: IFileSystemAdapter,
        github_adapter: IGitHubAdapter,
        git_adapter: IGitAdapter | None = None,
        roadmap_sync: RoadmapSyncUseCase | None = None,
        workflow_usecase: WorkflowUseCase | None = None,
    ):
        self.fs = fs_adapter
        self.github = github_adapter
        self.git = git_adapter
        self.roadmap_sync = roadmap_sync
        self.workflow = workflow_usecase

    def _parse_dependencies(self, doc: Document) -> set[str]:
        """Parse dependencies from document metadata."""
        depends_on = (
            doc.metadata.get("depends_on") or doc.metadata.get("Depends-On") or []
        )
        if isinstance(depends_on, str):
            if depends_on.lower() == "(none)":
                return set()
            depends_on = [d.strip() for d in depends_on.split(",")]
        return {str(d) for d in depends_on}

    def create_issues(
        self,
        before: str,
        after: str,
        adr_id: str | None = None,
        archive_path: str = "reqs/tasks/_archive/",
        roadmap_path: str | None = None,
        use_pr: bool = False,
        base_branch: str = "main",
    ) -> None:
        """
        Implementation of ADR-007 Issue Creation Logic.
        """
        if not self.git:
            raise RuntimeError("GitAdapter is required.")

        # Step 1: Discovery
        search_path = f"reqs/tasks/{adr_id}/" if adr_id else "reqs/tasks/"
        added_files = self.git.get_added_files(before, after, search_path)

        batch_docs: dict[str, Document] = {}
        path_map: dict[str, str] = {}

        for file_path in added_files:
            if not file_path.endswith(".md"):
                continue
            doc = self.fs.read_document(Path(file_path))
            doc_id = doc.metadata.get("id")
            if doc_id:
                batch_docs[doc_id] = doc
                path_map[doc_id] = file_path

        if not batch_docs:
            return

        # Step 2: DAG & Ready Judgment
        graph: dict[str, set[str]] = {}
        ready_tasks: dict[str, Document] = {}

        # Load archived tasks for dependency checking
        archived_docs: dict[str, Document] = {}
        for arch_file in self.fs.list_files(Path(archive_path), "*.md"):
            try:
                a_doc = self.fs.read_document(arch_file)
                a_id = a_doc.metadata.get("id")
                if a_id:
                    archived_docs[a_id] = a_doc
            except Exception:
                continue

        def is_ready(doc: Document) -> bool:
            deps = self._parse_dependencies(doc)
            for d_id in deps:
                # 1. Check if dependency is in the current batch
                if d_id in batch_docs:
                    continue
                # 2. Check if dependency is in archive
                if d_id in archived_docs:
                    a_doc = archived_docs[d_id]
                    if a_doc.metadata.get("status") in ["Issued", "Completed"]:
                        continue
                # 3. Check if it's already issued
                raise RuntimeError(
                    f"Missing dependency: {d_id} for task {doc.metadata.id}"
                )
            return True

        for doc_id, doc in batch_docs.items():
            if is_ready(doc):
                ready_tasks[doc_id] = doc
                deps = self._parse_dependencies(doc)
                graph[doc_id] = {d for d in deps if d in batch_docs}

        if not ready_tasks:
            print("No tasks are Ready for creation.")
            return

        ts = TopologicalSorter(graph)
        try:
            create_order = list(ts.static_order())
        except CycleError as e:
            raise CycleError(f"Circular dependency detected: {e}") from e

        # Step 3: Atomic Issue Creation (Fail-fast)
        issued_tasks: list[tuple[str, int, Document]] = []
        try:
            for doc_id in create_order:
                if doc_id not in ready_tasks:
                    continue
                doc = batch_docs[doc_id]

                title = doc.metadata.get("title") or doc_id
                body = doc.content
                labels = doc.metadata.get("labels", [])
                if isinstance(labels, str):
                    labels = [label.strip() for label in labels.split(",")]

                issue_id = self.github.create_issue(title, body, labels)

                # Update metadata in memory
                doc.metadata.update({"status": "Issued", "issue_id": issue_id})

                issued_tasks.append((doc_id, issue_id, doc))
        except Exception as e:
            # Step 3 Failure: abort before Step 4
            raise RuntimeError(f"Issue creation failed: {e}") from e

        # Step 4: Atomic Move & Status Transition
        processed_paths = []
        sync_results: list[tuple[Path, int]] = []
        for doc_id, issue_id, doc in issued_tasks:
            src_path = path_map[doc_id]
            dst_path = f"{archive_path}{Path(src_path).name}"

            # Update local file before move
            self.fs.save_document(Path(src_path), doc)

            # Atomic Move via git mv
            self.git.move_file(src_path, dst_path)
            processed_paths.append(dst_path)
            sync_results.append((Path(dst_path), issue_id))

        # Step 5: Roadmap Sync
        if self.roadmap_sync and roadmap_path:
            try:
                self.roadmap_sync.sync(roadmap_path, sync_results)
                processed_paths.append(roadmap_path)
            except Exception as e:
                print(f"Warning: Roadmap sync failed: {e}")

        # Step 6: Git Commit & Push
        if processed_paths:
            try:
                if use_pr:
                    timestamp = int(time.time())
                    sync_branch = f"chore/metadata-sync-{timestamp}"
                    print(f"Creating metadata sync branch: {sync_branch}")

                    self.git.fetch(remote="origin")
                    self.git.checkout(
                        sync_branch, create=True, base=f"origin/{base_branch}"
                    )
                    self.git.add(processed_paths)
                    self.git.commit("docs: update issue numbers and sync roadmap")
                    self.git.push(remote="origin", branch=sync_branch)

                    title = "chore: sync metadata for new issues"
                    body = "Automatic metadata update (issue numbers and roadmap sync) for newly created issues."
                    pr_url, pr_number = self.github.create_pull_request(
                        title, body, head=sync_branch, base=base_branch
                    )
                    self.github.add_labels(pr_number, ["metadata"])
                    print(f"Created metadata sync PR: {pr_url}")
                else:
                    current_branch = self.git.get_current_branch()
                    self.git.add(processed_paths)
                    self.git.commit("docs: update issue numbers and sync roadmap")
                    self.git.push(remote="origin", branch=current_branch)
            except Exception as e:
                print(f"Git operations failed: {e}")
                raise RuntimeError(f"Failed to record metadata changes: {e}") from e
