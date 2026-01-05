# ruff: noqa: T201
from graphlib import TopologicalSorter
from pathlib import Path

from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter


class IssueCreationUseCase:
    def __init__(
        self,
        fs_adapter: FileSystemAdapter,
        github_adapter: GitHubAdapter,
        git_adapter: GitAdapter | None = None,
    ):
        self.fs = fs_adapter
        self.github = github_adapter
        self.git = git_adapter

    def _get_dependencies(
        self, files: list[Path]
    ) -> tuple[dict[str, set[str]], dict[str, Path]]:
        graph = {}
        file_map = {}

        for file_path in files:
            filename = file_path.name
            file_map[filename] = file_path

            try:
                doc = self.fs.read_document(file_path)
            except Exception as e:
                print(f"Warning: Failed to parse {filename}: {e}")
                continue

            depends_on = doc.metadata.get("depends_on") or doc.metadata.get(
                "Depends-On"
            )

            deps = set()
            if depends_on:
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

            graph[filename] = deps

        return graph, file_map

    def create_issues_from_virtual_queue(
        self,
        base_ref: str,
        head_ref: str,
        archive_path: str = "reqs/tasks/archive/",
        roadmap_path: str | None = None,
    ) -> None:
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
            except Exception as e:
                print(f"Warning: Failed to parse {file_str}: {e}")

        if not target_docs:
            print("No new tasks to process.")
            return

        print(f"Processing {len(target_docs)} new tasks.")

        # 3. Dependency resolution
        # We can pass already read documents to a slightly modified _get_dependencies or just use its logic
        graph = {}
        file_map = {}  # {filename: Path}
        doc_map = {}  # {filename: Document}

        for path, doc in target_docs.items():
            filename = path.name
            file_map[filename] = path
            doc_map[filename] = doc

            depends_on = doc.metadata.get("depends_on") or doc.metadata.get(
                "Depends-On"
            )
            deps = set()
            if depends_on:
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
            graph[filename] = deps

        ts = TopologicalSorter(graph)
        try:
            create_order = list(ts.static_order())
        except Exception as e:
            raise ValueError(f"Error resolving dependencies: {e}") from e

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
                # Replace placeholders for dependencies
                for dep_filename, issue_num in issue_map.items():
                    body = body.replace(dep_filename, f"#{issue_num}")

                labels = doc.metadata.get("labels", [])
                if isinstance(labels, str):
                    labels = [label.strip() for label in labels.split(",")]

                print(f"Creating issue for: {title}")
                issue_number = self.github.create_issue(title, body, labels)
                print(f"Created issue #{issue_number}")
                results.append((path, issue_number))
                issue_map[filename] = issue_number
        except Exception as e:
            print(f"Error during issue creation: {e}")
            print("Fail-fast: Aborting without writing back to Git.")
            raise e

        # 5. Success: Write back
        processed_paths = []
        for path, issue_number in results:
            self.fs.update_metadata(path, {"issue": f"#{issue_number}"})
            processed_paths.append(str(path))

        # 6. Git Commit
        if processed_paths:
            self.git.add(processed_paths)
            self.git.commit("docs: update issue numbers")
