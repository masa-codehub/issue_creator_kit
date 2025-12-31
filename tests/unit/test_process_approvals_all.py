from unittest.mock import patch

import pytest

from issue_creator_kit.scripts import process_approvals


@pytest.fixture
def mock_dirs(tmp_path):
    inbox = tmp_path / "_inbox"
    approved = tmp_path / "_approved"
    inbox.mkdir()
    approved.mkdir()
    return inbox, approved


@patch("issue_creator_kit.scripts.process_approvals.process_single_file")
def test_process_all_files_success(mock_process_single, mock_dirs):
    inbox, approved = mock_dirs

    # Create dummy files
    (inbox / "doc1.md").touch()
    (inbox / "doc2.md").touch()

    result = process_approvals.process_all_files(
        inbox_dir=inbox,
        approved_dir=approved,
        repo_name="owner/repo",
        token="dummy_token",
    )

    assert result is True
    assert mock_process_single.call_count == 2
    # Check that it was called for both files
    # Note: glob order is not guaranteed, so we check using any_order or similar if strict
    # Here just checking count is a basic sanity check


@patch("issue_creator_kit.scripts.process_approvals.process_single_file")
def test_process_all_files_empty(mock_process_single, mock_dirs):
    inbox, approved = mock_dirs
    # No files

    result = process_approvals.process_all_files(
        inbox_dir=inbox,
        approved_dir=approved,
        repo_name="owner/repo",
        token="dummy_token",
    )

    assert result is False
    mock_process_single.assert_not_called()


@patch("issue_creator_kit.scripts.process_approvals.process_single_file")
def test_process_all_files_failure(mock_process_single, mock_dirs):
    inbox, approved = mock_dirs
    (inbox / "bad_doc.md").touch()

    # Simulate failure
    mock_process_single.side_effect = Exception("Processing failed")

    with pytest.raises(Exception, match="Processing failed"):
        process_approvals.process_all_files(
            inbox_dir=inbox,
            approved_dir=approved,
            repo_name="owner/repo",
            token="dummy_token",
        )
