# ruff: noqa: T201
import glob
import os
import re
import sys
from graphlib import TopologicalSorter

import requests

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


def parse_metadata(content):
    """
    Extracts metadata from the markdown content.
    Looks for lines starting with "- **Key**: Value".
    """
    metadata = {}
    for line in content.splitlines():
        match = re.match(r"^-\s*\*\*(.*?)\*\*:\s*(.*)", line)
        if match:
            key = match.group(1).strip()
            value = match.group(2).strip()
            metadata[key] = value
    return metadata


def get_dependencies(files):
    """
    Builds a dependency graph from the files.
    Returns:
        graph: {filename: {dependency_filename, ...}}
        file_map: {filename: full_path}
    """
    graph = {}
    file_map = {}

    for file_path in files:
        filename = os.path.basename(file_path)
        file_map[filename] = file_path

        with open(file_path, encoding="utf-8") as f:
            content = f.read()

        metadata = parse_metadata(content)
        depends_on = metadata.get("Depends-On", "")

        deps = set()
        if depends_on and depends_on.lower() != "(none)":
            # Remove parentheses if present (common in templates)
            depends_on = depends_on.replace("(", "").replace(")", "")
            # Split by comma
            for dep in depends_on.split(","):
                dep = dep.strip()
                if dep and dep.endswith(".md"):  # Basic validation
                    deps.add(dep)

        graph[filename] = deps

    return graph, file_map


def create_issue(filename, file_path, issue_map):
    """
    Creates a GitHub issue from the markdown file.
    Replaces dependency filenames with actual issue numbers in the body.
    """
    with open(file_path, encoding="utf-8") as f:
        content = f.read()

    # Extract Title (First line usually)
    title = filename  # Default fallback
    lines = content.splitlines()
    for line in lines:
        if line.startswith("# "):
            title = line[2:].strip()
            break

    # Prepare Body
    # Replace dependency filenames with Issue numbers
    body = content
    for dep_filename, issue_number in issue_map.items():
        # Replace "issue-XXX.md" with "#123"
        # Using simple string replacement. Could be more robust with regex if needed.
        body = body.replace(dep_filename, f"#{issue_number}")

    # GitHub API Payload
    data = {
        "title": title,
        "body": body,
        # Labels or assignees could be parsed from metadata if needed
    }

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
    # We process all files in reqs/_issues/ that are NOT in the archive directory yet.
    # Exclude directories.
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
        # static_order() returns an iterable of nodes in topological order
        # Nodes with no dependencies come first.
        create_order = list(ts.static_order())
    except Exception as e:
        print(f"Error resolving dependencies (Cycle detected?): {e}")
        # If there's a cycle, we can't strictly order them.
        # We might want to just proceed with best effort or fail.
        # For now, fail.
        sys.exit(1)

    # Filter out files that might have been in the graph keys but not in our target list (if any)
    # Though with logic above, all keys in graph come from 'files'.

    # 4. Create Issues in Order
    issue_map = {}  # {filename: issue_number}

    # Make sure archive dir exists
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)

    for filename in create_order:
        if filename not in file_map:
            # Could happen if a dependency is listed but the file doesn't exist in the folder.
            # In that case, we can't replace it with a number, just skip creating it (it's assumed already exists or missing).
            print(
                f"Warning: Dependency {filename} not found in current batch. Assuming it's external or already created."
            )
            continue

        file_path = file_map[filename]

        # Create Issue
        issue_number = create_issue(filename, file_path, issue_map)
        issue_map[filename] = issue_number

        # 5. Move to Archive
        # We don't use git mv here because this script runs inside the action,
        # and the workflow will handle the git commit/push of the file moves separately
        # OR we can do the move here on FS and let the workflow 'git add -A' later.
        # Let's do the FS move.
        target_path = os.path.join(ARCHIVE_DIR, filename)
        os.rename(file_path, target_path)
        print(f"Moved {filename} to {ARCHIVE_DIR}")


if __name__ == "__main__":
    main()
