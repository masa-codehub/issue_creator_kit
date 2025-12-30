import os
from unittest.mock import MagicMock, patch

import pytest

# Setup env vars before import
os.environ["GITHUB_REPOSITORY"] = "owner/repo"
os.environ["GH_TOKEN"] = "token"

from issue_creator_kit.scripts import create_issues


@pytest.fixture
def mock_utils():
    with patch("issue_creator_kit.scripts.create_issues.utils") as mock:
        yield mock


def test_get_dependencies_yaml(tmp_path, mock_utils):
    # Setup files with YAML frontmatter
    # However, since we are mocking utils.load_document, the actual file content matters less
    # BUT get_dependencies currently opens the file.
    # Refactoring will change it to use utils.load_document.

    file1 = tmp_path / "issue-1.md"
    file2 = tmp_path / "issue-2.md"

    file1.touch()
    file2.touch()

    # Mock utils.load_document return values
    mock_utils.load_document.side_effect = [
        ({"title": "Issue 1", "depends_on": ["issue-2.md"]}, "# Body 1"),
        ({"title": "Issue 2", "depends_on": []}, "# Body 2"),
    ]

    files = [str(file1), str(file2)]

    graph, file_map = create_issues.get_dependencies(files)

    assert "issue-1.md" in graph
    assert "issue-2.md" in graph
    assert "issue-2.md" in graph["issue-1.md"]
    assert len(graph["issue-2.md"]) == 0


def test_create_issue_replace_links(tmp_path, mock_utils):
    # Test body replacement
    file_path = tmp_path / "issue-1.md"
    file_path.write_text("Depends on issue-2.md", encoding="utf-8")

    # Mock requests
    with patch("issue_creator_kit.scripts.create_issues.requests") as mock_requests:
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"number": 101}
        mock_requests.post.return_value = mock_response

        issue_map = {"issue-2.md": 202}

        # We need to make sure create_issue uses utils.load_document if we refactor it
        # Current implementation opens file directly.
        # So for this test to pass AFTER refactoring, we need to mock utils.load_document if used.
        # But create_issue logic currently reads file again.

        # If I refactor create_issue to use utils.load_document, I should mock it.
        mock_utils.load_document.return_value = (
            {"title": "Issue 1"},
            "Depends on issue-2.md",
        )

        create_issues.create_issue("issue-1.md", str(file_path), issue_map)

        # Check payload
        call_args = mock_requests.post.call_args[1]
        data = call_args["json"]
        assert "Depends on #202" in data["body"]
