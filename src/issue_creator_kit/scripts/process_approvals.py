import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

from github import Github

import issue_creator_kit.utils as utils


def process_single_file(
    file_path: Path, approved_dir: Path, repo_name: str, token: str
) -> None:
    """
    Process a single document for approval.

    1. Load document
    2. Update Status to 'Approved' and Date to today
    3. Move to approved_dir
    4. Create GitHub Issue
    5. Update document with Issue number
    """

    # 1. Load document
    # We verify existence via load_document (which raises FileNotFoundError)
    metadata, content = utils.load_document(file_path)
    title = metadata.get("title", file_path.stem)

    # 2. Update Status and Date
    updates = {"status": "Approved", "date": datetime.now().strftime("%Y-%m-%d")}
    # Check for "Last Updated" key variation
    if "Last Updated" in metadata:
        updates["Last Updated"] = updates["date"]

    utils.update_metadata(file_path, updates)

    # 3. Move file
    moved_path = utils.safe_move_file(file_path, approved_dir)
    print(f"Moved file to: {moved_path}")

    # 4. Create GitHub Issue
    g = Github(token)
    repo = g.get_repo(repo_name)

    # Use the path relative to project root for the body link if possible
    # Assuming running from root, moved_path is relative
    relative_path = str(moved_path)

    issue_body = (
        f"Tracking issue for approved document: {relative_path}\n\n"
        f"Original Content Summary:\n{content[:200]}..."
    )

    issue = repo.create_issue(
        title=title, body=issue_body, labels=["documentation", "approved"]
    )
    print(f"Created Issue #{issue.number}")

    # 5. Update Issue Number
    utils.update_metadata(moved_path, {"issue": f"#{issue.number}"})
    print(f"Updated document with Issue #{issue.number}")


def main():
    parser = argparse.ArgumentParser(description="Process approved documents.")
    parser.add_argument("file_path", type=Path, help="Path to the document to approve")
    parser.add_argument(
        "--approved-dir",
        type=Path,
        default=Path("reqs/design/_approved"),
        help="Directory to move approved files",
    )
    parser.add_argument("--repo", required=True, help="GitHub Repository (owner/repo)")
    parser.add_argument(
        "--token", default=os.environ.get("GITHUB_TOKEN"), help="GitHub Token"
    )

    args = parser.parse_args()

    if not args.token:
        print("Error: GitHub Token is required (via --token or GITHUB_TOKEN env var)")
        sys.exit(1)

    try:
        process_single_file(args.file_path, args.approved_dir, args.repo, args.token)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
