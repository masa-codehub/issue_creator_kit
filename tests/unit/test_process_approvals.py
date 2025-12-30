from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from issue_creator_kit.scripts import process_approvals


@pytest.fixture
def mock_utils():
    with patch("issue_creator_kit.scripts.process_approvals.utils") as mock:
        yield mock


@pytest.fixture
def mock_github():
    with patch("issue_creator_kit.scripts.process_approvals.Github") as mock:
        yield mock


def test_process_approval_success(mock_utils, mock_github):
    # Setup
    file_path = Path("reqs/design/_inbox/test.md")
    approved_dir = Path("reqs/design/_approved")

    # Mock load_document
    mock_utils.load_document.return_value = (
        {"title": "Test Doc", "status": "Draft"},
        "# Content",
    )

    # Mock move
    moved_path = approved_dir / "test.md"
    mock_utils.safe_move_file.return_value = moved_path

    # Mock GitHub
    mock_repo = MagicMock()
    mock_issue = MagicMock()
    mock_issue.number = 123
    mock_repo.create_issue.return_value = mock_issue
    mock_github.return_value.get_repo.return_value = mock_repo

    # Execute
    process_approvals.process_single_file(
        file_path, approved_dir, repo_name="owner/repo", token="token"
    )

    # Verify
    # 1. Update Status
    # Get the first call to update_metadata
    first_call_args = mock_utils.update_metadata.call_args_list[0]
    args, _ = first_call_args
    assert args[0] == file_path
    assert args[1]["status"] == "Approved"
    assert "date" in args[1]

    # 2. Move File
    mock_utils.safe_move_file.assert_called_with(file_path, approved_dir)

    # 3. Create Issue
    mock_repo.create_issue.assert_called_once()
    call_args = mock_repo.create_issue.call_args[1]
    assert call_args["title"] == "Test Doc"
    assert "reqs/design/_approved/test.md" in call_args["body"]

    # 4. Update Issue Number in Moved File
    mock_utils.update_metadata.assert_called_with(moved_path, {"issue": "#123"})


def test_process_approval_file_not_found(mock_utils):
    file_path = Path("non_existent.md")
    mock_utils.load_document.side_effect = FileNotFoundError

    with pytest.raises(FileNotFoundError):
        process_approvals.process_single_file(
            file_path, Path("dst"), "owner/repo", "token"
        )
