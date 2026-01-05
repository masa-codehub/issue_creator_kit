# ruff: noqa: T201
import re
from pathlib import Path

from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter


class RoadmapSyncUseCase:
    """
    UseCase for synchronizing roadmap WBS links after issues are created.
    """

    def __init__(self, fs_adapter: FileSystemAdapter):
        self.fs = fs_adapter

    def sync(self, roadmap_path: str, results: list[tuple[Path, int]]) -> None:
        """
        Synchronize roadmap WBS links by replacing 'drafts' with 'archive'
        and appending the issue number.

        Args:
            roadmap_path (str): Path to the roadmap Markdown file. The file is
                expected to contain Markdown tables with links to task files.
            results (list[tuple[Path, int]]): A list of tuples where each tuple
                contains (archived_task_file_path, created_issue_number).

        Raises:
            ValueError: If a link for a task is not found in the roadmap,
                or if the URL format does not contain the expected 'drafts/' segment.
            FileNotFoundError: If the roadmap file does not exist.
        """
        if not results:
            return

        path = Path(roadmap_path)
        if not path.exists():
            raise FileNotFoundError(f"Roadmap file not found: {roadmap_path}")

        content = self.fs.read_file(str(path))
        new_content = content

        # Avoid redundant sync if results contain duplicate filenames
        seen_filenames = set()
        unique_results = []
        for file_path, issue_number in results:
            if file_path.name in seen_filenames:
                print(
                    f"Warning: Duplicate task filename {file_path.name} in results. Skipping."
                )
                continue
            seen_filenames.add(file_path.name)
            unique_results.append((file_path, issue_number))

        for file_path, issue_number in unique_results:
            filename = file_path.name

            # Look for link: [filename.md](url).
            # Using a more robust pattern to handle potential nested parentheses in URL.
            link_pattern = rf"\[{re.escape(filename)}\]\(([^)]+)\)"

            # Check if link exists
            if not re.search(link_pattern, new_content):
                raise ValueError(
                    f"Link for {filename} not found in roadmap {roadmap_path}"
                )

            def replace_link(
                match: re.Match, f: str = filename, n: int = issue_number
            ) -> str:
                url = match.group(1)

                # Validate and replace 'drafts' with 'archive' using path segments
                parts = url.split("/")
                found = False
                for i, part in enumerate(parts):
                    if part == "drafts":
                        parts[i] = "archive"
                        found = True
                        break

                if not found:
                    # If already archived, just ensure issue number is present
                    if "archive" in parts:
                        if f"(#{n})" in match.group(0):
                            return match.group(0)
                        return f"[{f}]({url}) (#{n})"

                    raise ValueError(
                        f"Expected 'drafts/' in URL for {f} in roadmap {roadmap_path}, but got: {url}"
                    )

                new_url = "/".join(parts)
                return f"[{f}]({new_url}) (#{n})"

            new_content = re.sub(link_pattern, replace_link, new_content)

        if new_content != content:
            self.fs.write_file(str(path), new_content)
            print(f"Updated roadmap: {roadmap_path}")
        else:
            print(f"No changes made to roadmap: {roadmap_path}")
