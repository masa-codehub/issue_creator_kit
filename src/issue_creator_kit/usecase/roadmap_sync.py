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
            roadmap_path (str): Path to the roadmap Markdown file.
            results (list[tuple[Path, int]]): A list of tuples, each containing
                the Path to the archived task file and its created issue number.

        Raises:
            ValueError: If a link for a processed task is not found in the roadmap,
                or if the URL format in the roadmap is unexpected.
            FileNotFoundError: If the roadmap file does not exist.
        """
        if not results:
            return

        path = Path(roadmap_path)
        if not path.exists():
            raise FileNotFoundError(f"Roadmap file not found: {roadmap_path}")

        content = self.fs.read_file(str(path))
        new_content = content

        # Check for duplicate filenames in results to avoid redundant processing
        seen_filenames = set()
        unique_results = []
        for file_path, issue_number in results:
            if file_path.name in seen_filenames:
                print(
                    f"Warning: Duplicate task filename detected: {file_path.name}. Skipping redundant sync."
                )
                continue
            seen_filenames.add(file_path.name)
            unique_results.append((file_path, issue_number))

        for file_path, issue_number in unique_results:
            filename = file_path.name

            # Look for link: [filename.md](url)
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

                # Robust validation: ensure it's a draft link
                if "drafts/" not in url:
                    # If it's already archived, we might want to just update the number
                    # but usually this means something is wrong or already processed.
                    if "archive/" in url:
                        # Update number if not present or different?
                        # For now, let's just append if missing.
                        if f"(#{n})" in url or f"(#{n})" in match.group(0):
                            return match.group(0)
                        return f"[{f}]({url}) (#{n})"

                    raise ValueError(
                        f"Expected 'drafts/' in URL for {f} in roadmap {roadmap_path}, but got: {url}"
                    )

                # Replace 'drafts' with 'archive' in the URL using regex for safety
                # Guaranteed to replace only when preceded by '/' or start of string
                new_url = re.sub(r"(?<=/)tasks/drafts/", "tasks/archive/", url)
                if new_url == url:
                    # Fallback if 'tasks/' prefix is missing
                    new_url = url.replace("drafts/", "archive/", 1)

                return f"[{f}]({new_url}) (#{n})"

            new_content = re.sub(link_pattern, replace_link, new_content)

        if new_content != content:
            self.fs.write_file(str(path), new_content)
            print(f"Updated roadmap: {roadmap_path}")
        else:
            print(f"No changes made to roadmap: {roadmap_path}")
