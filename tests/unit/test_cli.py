import sys
from unittest.mock import patch

import pytest

from issue_creator_kit import cli


def test_process_diff_command_with_adr_id():
    """Test 'process-diff' command with --adr-id."""
    with (
        patch("issue_creator_kit.cli.FileSystemAdapter"),
        patch("issue_creator_kit.cli.GitHubAdapter"),
        patch("issue_creator_kit.cli.GitAdapter"),
        patch("issue_creator_kit.cli.RoadmapSyncUseCase"),
        patch("issue_creator_kit.cli.IssueCreationUseCase") as mock_creation,
    ):
        before = "HEAD~1"
        after = "HEAD"
        adr_id = "adr-007"
        test_args = [
            "process-diff",
            "--before",
            before,
            "--after",
            after,
            "--adr-id",
            adr_id,
        ]

        with patch.object(sys, "argv", ["issue-kit"] + test_args):
            cli.main()

        # Verify create_issues called with adr_id
        mock_creation.return_value.create_issues.assert_called_once()
        call_kwargs = mock_creation.return_value.create_issues.call_args.kwargs
        assert call_kwargs["before"] == before
        assert call_kwargs["after"] == after
        assert call_kwargs["adr_id"] == adr_id
        # Check default archive_dir
        assert call_kwargs["archive_path"] == "reqs/tasks/_archive/"


def test_process_diff_command_without_adr_id():
    """Test 'process-diff' command without --adr-id."""
    with (
        patch("issue_creator_kit.cli.FileSystemAdapter"),
        patch("issue_creator_kit.cli.GitHubAdapter"),
        patch("issue_creator_kit.cli.GitAdapter"),
        patch("issue_creator_kit.cli.RoadmapSyncUseCase"),
        patch("issue_creator_kit.cli.IssueCreationUseCase") as mock_creation,
    ):
        test_args = [
            "process-diff",
            "--before",
            "HEAD~1",
            "--after",
            "HEAD",
        ]

        with patch.object(sys, "argv", ["issue-kit"] + test_args):
            cli.main()

        mock_creation.return_value.create_issues.assert_called_once()
        call_kwargs = mock_creation.return_value.create_issues.call_args.kwargs
        assert call_kwargs["adr_id"] is None


def test_process_diff_invalid_adr_id():
    """Test 'process-diff' with invalid --adr-id format."""
    test_args = [
        "process-diff",
        "--before",
        "HEAD~1",
        "--after",
        "HEAD",
        "--adr-id",
        "invalid-id",
    ]

    with (
        patch("sys.stderr"),  # Suppress error output during test
        patch.object(sys, "argv", ["issue-kit"] + test_args),
    ):
        with pytest.raises(SystemExit) as excinfo:
            cli.main()
        assert excinfo.value.code == 2  # argparse exits with 2 for invalid types
