# ruff: noqa: T201
import contextlib
import re
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

from issue_creator_kit.domain.document import Document
from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter
from issue_creator_kit.usecase.roadmap_sync import RoadmapSyncUseCase
from issue_creator_kit.usecase.workflow import WorkflowUseCase


class IssueCreationUseCase:
    """
    UseCase for detecting new tasks in the virtual queue and creating GitHub Issues.
    """

    def __init__(
        self,
        fs_adapter: FileSystemAdapter,
        github_adapter: GitHubAdapter,
        git_adapter: GitAdapter | None = None,
        roadmap_sync: RoadmapSyncUseCase | None = None,
        workflow_usecase: WorkflowUseCase | None = None,
    ):
        self.fs = fs_adapter
        self.github = github_adapter
        self.git = git_adapter
        self.roadmap_sync = roadmap_sync
        self.workflow = workflow_usecase

    def _parse_dependencies(self, doc: Document) -> set[str]:
        """Parse dependencies from document metadata and return a set of filenames."""
        depends_on = doc.metadata.get("depends_on") or doc.metadata.get("Depends-On")
        deps: set[str] = set()
        if not depends_on:
            return deps

        if isinstance(depends_on, list):
            for dep in depends_on:
                if isinstance(dep, str) and dep.endswith(".md"):
                    deps.add(Path(dep).name)
        elif isinstance(depends_on, str) and depends_on.lower() != "(none)":
            cleaned = depends_on.replace("(", "").replace(")", "")
            for dep in cleaned.split(","):
                dep = dep.strip()
                if dep and dep.endswith(".md"):
                    deps.add(Path(dep).name)
        return deps

    def _get_dependencies(
        self, files: list[Path]
    ) -> tuple[dict[str, set[str]], dict[str, Path]]:
        """Analyze dependencies between files and return a graph and file mapping."""
        graph = {}
        file_map = {}

        for file_path in files:
            filename = file_path.name
            file_map[filename] = file_path

            try:
                doc = self.fs.read_document(file_path)
                graph[filename] = self._parse_dependencies(doc)
            except (FileNotFoundError, PermissionError) as e:
                print(f"Error: Failed to access {file_path}: {e}")
                continue
            except Exception as e:
                print(f"Warning: Failed to parse {filename}: {e}")
                continue

        return graph, file_map

    def create_issues_from_virtual_queue(
        self,
        base_ref: str,
        head_ref: str,
        archive_path: str = "reqs/tasks/archive/",
        roadmap_path: str | None = None,
    ) -> None:
        """
        Detect added files in the archive path via git diff-tree, create GitHub issues,
        update file metadata with issue numbers, and optionally sync the roadmap.

        Flow:
        1. Detect added .md files in the virtual queue (archive_path).
        2. Resolve dependencies between tasks using Topological Sort.
        3. Create GitHub Issues in order, replacing task-ID placeholders with #IssueNo.
        4. If all issues are created successfully, update file metadata.
        5. Synchronize the roadmap WBS links if roadmap_path is provided.
        6. Commit and push the changes to Git.

        Args:
            base_ref (str): The base commit/branch for comparison.
            head_ref (str): The head commit/branch for comparison.
            archive_path (str): The directory path to monitor for new tasks.
            roadmap_path (str, optional): Path to the roadmap file to synchronize.

        Raises:
            RuntimeError: If GitAdapter is missing or if issue creation fails.
            ValueError: If task dependencies contain cycles.
        """
        if not self.git:
            raise RuntimeError("GitAdapter is required for virtual queue.")

        # 1. Detect added files in archive/
        added_files = self.git.get_added_files(base_ref, head_ref, archive_path)
        print(f"Detected {len(added_files)} added files in {archive_path}")

        # 2. Filter .md files and check issue metadata (DifferenceDetector)
        target_docs = {}  # {Path: Document}
        for file_str in added_files:
            if not file_str.endswith(".md"):
                continue
            path = Path(file_str)
            try:
                doc = self.fs.read_document(path)
                if not doc.metadata.get("issue"):
                    target_docs[path] = doc
            except (FileNotFoundError, PermissionError) as e:
                # Fatal: Cannot proceed if we can't access files we know exist in git
                print(f"Error: Failed to access {file_str}: {e}")
                raise
            except Exception as e:
                # Non-fatal: Skip malformed files but log warning
                print(f"Warning: Failed to parse {file_str}: {e}")

        if not target_docs:
            print("No new tasks to process.")
            return

        print(f"Processing {len(target_docs)} new tasks.")

        # 3. Dependency resolution
        graph = {}
        file_map = {}  # {filename: Path}
        doc_map = {}  # {filename: Document}

        for path, doc in target_docs.items():
            filename = path.name
            file_map[filename] = path
            doc_map[filename] = doc
            graph[filename] = self._parse_dependencies(doc)

        ts = TopologicalSorter(graph)
        try:
            create_order = list(ts.static_order())
        except CycleError as e:
            raise ValueError(
                f"Error resolving dependencies (cycle detected): {e}"
            ) from e

        # 4. Atomic Batch Creation
        results = []
        issue_map: dict[str, int] = {}  # {filename: issue_number}
        try:
            for filename in create_order:
                if filename not in file_map:
                    continue
                path = file_map[filename]
                doc = doc_map[filename]

                title = doc.metadata.get("title") or path.stem
                body = doc.content
                # Replace placeholders for dependencies using regex with word boundaries
                # to avoid accidental partial matches.
                for dep_filename, issue_num in issue_map.items():
                    # Replace 'task-ID.md' with '#IssueNo'
                    pattern = rf"\b{re.escape(dep_filename)}\b"
                    body = re.sub(pattern, f"#{issue_num}", body)

                labels = doc.metadata.get("labels", [])
                if isinstance(labels, str):
                    labels = [label.strip() for label in labels.split(",")]

                print(f"Creating issue for: {title}")
                issue_number = self.github.create_issue(title, body, labels)
                print(f"Created issue #{issue_number}")
                results.append((path, issue_number))
                issue_map[filename] = issue_number
        except RuntimeError as e:
            print(
                f"Error during issue creation (fail-fast, aborting without writing back to Git): {e}"
            )
            raise

        # 5. Success: Write back
        processed_paths = []
        for path, issue_number in results:
            self.fs.update_metadata(path, {"issue": f"#{issue_number}"})
            processed_paths.append(str(path))

        # 6. Roadmap Sync (Dynamic)
        roadmap_groups: dict[str, list[tuple[Path, int]]] = {}
        if roadmap_path:
            roadmap_groups[roadmap_path] = []

        next_phases = set()

        for path, issue_number in results:
            target_doc = doc_map.get(path.name)
            if not target_doc:
                continue

            # Roadmap Grouping
            r_path = target_doc.metadata.get("roadmap_path")
            if r_path:
                if r_path not in roadmap_groups:
                    roadmap_groups[r_path] = []
                roadmap_groups[r_path].append((path, issue_number))
            elif roadmap_path:
                # Fallback to default roadmap if not specified in doc
                # Avoid duplication if logic already added it?
                # Using set to avoid duplicates in list? sync() handles duplicates but better here.
                # However, tuples are (path, int), so unique per task.
                roadmap_groups[roadmap_path].append((path, issue_number))

            # Next Phase Detection
            np = target_doc.metadata.get("next_phase_path")
            if np:
                next_phases.add(np)

        if self.roadmap_sync:
            for r_path, r_results in roadmap_groups.items():
                if not r_results:
                    continue
                try:
                    self.roadmap_sync.sync(r_path, r_results)
                    processed_paths.append(r_path)
                except Exception as e:
                    print(f"Warning: Failed to sync roadmap at {r_path}: {e}")

        # 7. Git Commit
        if processed_paths:
            try:
                self.git.add(processed_paths)
                self.git.commit("docs: update issue numbers and sync roadmap")
            except Exception as e:
                print(f"Error during git commit: {e}")
                raise

                # 8. Auto-PR (Phase Promotion)
                if self.workflow and next_phases:
                    for np_path in next_phases:
                        try:
                            print(f"Triggering Auto-PR for next phase: {np_path}")
                            self.workflow.promote_next_phase(np_path)

                            # Switch back to main to ensure subsequent logic (like pushing changes) works
                            self.git.checkout("main")

                        except Exception as e:
                            print(
                                f"Error calling promote_next_phase for {np_path}: {e}"
                            )
                            # Try to recover state
                            with contextlib.suppress(Exception):
                                self.git.checkout("main")
