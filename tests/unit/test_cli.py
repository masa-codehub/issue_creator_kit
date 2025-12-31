import sys
from pathlib import Path
from unittest.mock import patch

import pytest

from issue_creator_kit import cli


def test_approve_command(tmp_path):
    """Test that 'approve' command calls process_single_file with correct args."""

    # Create a dummy file
    dummy_file = tmp_path / "test_doc.md"
    dummy_file.touch()

    with (
        patch(
            "issue_creator_kit.scripts.process_approvals.process_single_file"
        ) as mock_process,
        patch.dict(
            "os.environ",
            {"GITHUB_REPOSITORY": "test/repo", "GITHUB_TOKEN": "test_token"},
        ),
    ):
        # Simulate CLI args
        test_args = ["approve", str(dummy_file)]
        with patch.object(sys, "argv", ["issue-kit"] + test_args):
            cli.main()

        mock_process.assert_called_once()
        call_args = mock_process.call_args
        # process_single_file uses file_path as first arg, but we should check how it is called.
        # If called with keywords:
        if "file_path" in call_args.kwargs:
            assert call_args.kwargs["file_path"] == Path(dummy_file)
        else:
            # If positional
            assert call_args.args[0] == Path(dummy_file)

        assert call_args.kwargs.get("repo_name") == "test/repo"
        assert call_args.kwargs.get("token") == "test_token"


def test_approve_command_custom_args(tmp_path):
    """Test 'approve' command with custom --repo and --token."""
    dummy_file = tmp_path / "test_doc.md"
    dummy_file.touch()

    with patch(
        "issue_creator_kit.scripts.process_approvals.process_single_file"
    ) as mock_process:
        test_args = [
            "approve",
            str(dummy_file),
            "--repo",
            "custom/repo",
            "--token",
            "custom_token",
        ]
        with patch.object(sys, "argv", ["issue-kit"] + test_args):
            cli.main()

        mock_process.assert_called_once()
        assert mock_process.call_args.kwargs.get("repo_name") == "custom/repo"
        assert mock_process.call_args.kwargs.get("token") == "custom_token"


def test_approve_command_missing_env(tmp_path):
    """Test failure when repo/token are missing."""
    dummy_file = tmp_path / "test_doc.md"
    dummy_file.touch()

    # Ensure no env vars
    with patch.dict("os.environ", {}, clear=True):
        test_args = ["approve", str(dummy_file)]
        with patch.object(sys, "argv", ["issue-kit"] + test_args):
            with pytest.raises(SystemExit) as excinfo:
                cli.main()
            assert excinfo.value.code == 1
