# ruff: noqa: T201
from graphlib import TopologicalSorter
from pathlib import Path

from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter


class IssueCreationUseCase:
    def __init__(self, fs_adapter: FileSystemAdapter, github_adapter: GitHubAdapter):
        self.fs = fs_adapter
        self.github = github_adapter

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

    def create_issues_from_queue(self, queue_dir: Path, archive_dir: Path):
        # 1. Identify files (recursively)
        # Note: glob pattern "**/*.md" is needed for recursive search
        files = list(queue_dir.rglob("*.md"))
        files = [f for f in files if f.is_file()]

        if not files:
            print("No issue files found in queue.")
            return

        print(f"Found {len(files)} files to process.")

        # 2. Build Dependency Graph
        graph, file_map = self._get_dependencies(files)

        # 3. Topological Sort
        ts = TopologicalSorter(graph)
        try:
            create_order = list(ts.static_order())
        except Exception as e:
            raise ValueError(
                f"Error resolving dependencies (Cycle detected?): {e}"
            ) from e

        # 4. Create Issues
        issue_map: dict[str, int] = {}  # {filename: issue_number}

        for filename in create_order:
            if filename not in file_map:
                continue

            file_path = file_map[filename]

            # Create Issue
            doc = self.fs.read_document(file_path)

            # Determine Title
            title = doc.metadata.get("title")
            if not title:
                for line in doc.content.splitlines():
                    if line.startswith("# "):
                        title = line[2:].strip()
                        break
            if not title:
                title = filename

            # Replace Placeholders
            body = doc.content
            for dep_filename, issue_number in issue_map.items():
                body = body.replace(dep_filename, f"#{issue_number}")

            # Determine Labels
            labels = []
            if "labels" in doc.metadata:
                lbls = doc.metadata["labels"]
                if isinstance(lbls, list):
                    labels = [lbl for lbl in lbls if isinstance(lbl, str)]
                elif isinstance(lbls, str):
                    labels = [lbl.strip() for lbl in lbls.split(",")]

            print(f"Creating issue for {filename}...")
            try:
                issue_number = self.github.create_issue(title, body, labels)
                print(f"Success! Created issue #{issue_number} for {filename}")
                issue_map[filename] = issue_number
            except Exception as e:
                print(f"Failed to create issue for {filename}: {e}")
                # Fail-fast
                raise e

            # 5. Archive
            try:
                rel_path = file_path.relative_to(queue_dir)
                target_dir = archive_dir / rel_path.parent

                self.fs.safe_move_file(file_path, target_dir, overwrite=True)
                print(f"Moved {filename} to {target_dir}")

                archived_path = target_dir / filename
                self.fs.update_metadata(archived_path, {"issue": f"#{issue_number}"})

            except Exception as e:
                print(f"Error archiving {filename}: {e}")
                raise e
