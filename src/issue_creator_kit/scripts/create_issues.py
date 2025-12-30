# ruff: noqa: T201
import glob
import os
import sys
from graphlib import TopologicalSorter
from pathlib import Path

import requests

import issue_creator_kit.utils as utils

# Configuration
ISSUES_DIR = "reqs/_issues"
ARCHIVE_DIR = "reqs/_issues/created"
REPO = os.environ.get("GITHUB_REPOSITORY")  # e.g., "owner/repo"
TOKEN = os.environ.get("GH_TOKEN")
API_URL = f"https://api.github.com/repos/{REPO}/issues"

if not REPO or not TOKEN:
    print("Error: GITHUB_REPOSITORY or GH_TOKEN environment variable is missing.")
    sys.exit(1)

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
}


def get_dependencies(files):
    """
    Builds a dependency graph from the files using YAML metadata.
    Returns:
        graph: {filename: {dependency_filename, ...}}
        file_map: {filename: full_path}
    """
    graph = {}
    file_map = {}

    for file_path_str in files:
        file_path = Path(file_path_str)
        filename = file_path.name
        file_map[filename] = str(file_path)

        try:
            metadata, _ = utils.load_document(file_path)
        except Exception as e:
            print(f"Warning: Failed to parse {filename}: {e}")
            continue

        # Support both 'depends_on' (new) and 'Depends-On' (legacy)
        depends_on = metadata.get("depends_on") or metadata.get("Depends-On")

        deps = set()
        if depends_on:
            if isinstance(depends_on, list):
                # New YAML list format
                for dep in depends_on:
                    if dep and dep.endswith(".md"):
                        deps.add(dep)
            elif isinstance(depends_on, str) and depends_on.lower() != "(none)":
                # Legacy string format or string in YAML
                cleaned = depends_on.replace("(", "").replace(")", "")
                for dep in cleaned.split(","):
                    dep = dep.strip()
                    if dep and dep.endswith(".md"):
                        deps.add(dep)

        graph[filename] = deps

    return graph, file_map


def create_issue(filename, file_path_str, issue_map):
    """
    Creates a GitHub issue from the markdown file.
    Replaces dependency filenames with actual issue numbers in the body.
    """
    file_path = Path(file_path_str)
    try:
        metadata, content = utils.load_document(file_path)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
        sys.exit(1)

    # Extract Title: Metadata > H1 in content > filename
    title = metadata.get("title")
    if not title:
        for line in content.splitlines():
            if line.startswith("# "):
                title = line[2:].strip()
                break
    if not title:
        title = filename

    # Prepare Body
    # Replace dependency filenames with Issue numbers
    body = content
    for dep_filename, issue_number in issue_map.items():
        # Replace "issue-XXX.md" with "#123"
        body = body.replace(dep_filename, f"#{issue_number}")

    # GitHub API Payload
    data = {
        "title": title,
        "body": body,
        # Labels or assignees could be parsed from metadata if needed
        # e.g., labels: metadata.get("labels", [])
    }

    if "labels" in metadata:
        labels = metadata["labels"]
        if isinstance(labels, list):
            data["labels"] = labels
        elif isinstance(labels, str):
            data["labels"] = [lbl.strip() for lbl in labels.split(",")]

    print(f"Creating issue for {filename}...")
    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 201:
        issue = response.json()
        issue_number = issue["number"]
        print(f"Success! Created issue #{issue_number} for {filename}")
        return issue_number
    print(f"Failed to create issue for {filename}. Status: {response.status_code}")
    print(response.text)
    sys.exit(1)


def main():
    # 1. Identify target files
    files = [
        f for f in glob.glob(os.path.join(ISSUES_DIR, "*.md")) if os.path.isfile(f)
    ]

    if not files:
        print("No issue files found in inbox.")
        return

    print(f"Found {len(files)} files to process.")

    # 2. Build Dependency Graph
    graph, file_map = get_dependencies(files)

    # 3. Topological Sort
    ts = TopologicalSorter(graph)
    try:
        create_order = list(ts.static_order())
    except Exception as e:
        print(f"Error resolving dependencies (Cycle detected?): {e}")
        sys.exit(1)

    # 4. Create Issues in Order
    issue_map = {}  # {filename: issue_number}

    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    for filename in create_order:
        if filename not in file_map:
            print(
                f"Warning: Dependency {filename} not found in current batch. Assuming it's external or already created."
            )
            continue

        file_path_str = file_map[filename]

        # Create Issue
        issue_number = create_issue(filename, file_path_str, issue_map)
        issue_map[filename] = issue_number

        # 5. Move to Archive
        # Using utils.safe_move_file would be better, but keeping it simple for now as per refactoring scope
        # Actually, let's use utils.safe_move_file if we are refactoring!
        try:
            utils.safe_move_file(Path(file_path_str), Path(ARCHIVE_DIR), overwrite=True)
            print(f"Moved {filename} to {ARCHIVE_DIR}")
        except Exception as e:
            print(f"Error moving {filename}: {e}")


if __name__ == "__main__":
    main()
