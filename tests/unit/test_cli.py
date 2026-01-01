import os
import sys
from pathlib import Path
from unittest.mock import mock_open, patch

from issue_creator_kit import cli


def test_run_workflow_command():
    """Test 'run-workflow' command execution."""
    with (
        patch("issue_creator_kit.cli.FileSystemAdapter") as mock_fs,
        patch("issue_creator_kit.cli.GitHubAdapter") as mock_github,
        patch("issue_creator_kit.cli.GitAdapter") as mock_git,
        patch("issue_creator_kit.cli.ApprovalUseCase") as mock_approval,
        patch("issue_creator_kit.cli.WorkflowUseCase") as mock_workflow,
    ):
        # Setup args
        inbox = "reqs/design/_inbox"
        approved = "reqs/design/_approved"
        branch = "auto-approve/docs"

        test_args = [
            "run-workflow",
            "--inbox-dir",
            inbox,
            "--approved-dir",
            approved,
            "--branch",
            branch,
        ]

        with patch.object(sys, "argv", ["issue-kit"] + test_args):
            cli.main()

        # Verify instantiation
        mock_fs.assert_called_once()
        mock_github.assert_called_once()
        mock_git.assert_called_once()

        # Verify UseCase instantiation
        mock_approval.assert_called_once_with(
            mock_fs.return_value, mock_github.return_value
        )
        mock_workflow.assert_called_once_with(
            mock_approval.return_value, mock_git.return_value
        )

        # Verify run called with correct args
        mock_workflow.return_value.run.assert_called_once()
        call_kwargs = mock_workflow.return_value.run.call_args.kwargs

        # Check args
        assert call_kwargs["inbox_dir"] == Path(inbox)
        assert call_kwargs["approved_dir"] == Path(approved)
        assert call_kwargs["branch_name"] == branch


def test_run_workflow_outputs():
    """Test that run-workflow writes to GITHUB_OUTPUT."""
    with (
        patch("issue_creator_kit.cli.WorkflowUseCase") as mock_workflow,
        patch("issue_creator_kit.cli.FileSystemAdapter"),
        patch("issue_creator_kit.cli.GitHubAdapter"),
        patch("issue_creator_kit.cli.GitAdapter"),
        patch("issue_creator_kit.cli.ApprovalUseCase"),
        patch.dict(os.environ, {"GITHUB_OUTPUT": "/tmp/output"}),
        patch("builtins.open", mock_open()) as mock_file,
    ):
        # Case 1: Changes (True)
        mock_workflow.return_value.run.return_value = True
        test_args = ["run-workflow", "--branch", "test"]
        with patch.object(sys, "argv", ["issue-kit"] + test_args):
            cli.main()

        mock_file().write.assert_called_with("has_changes=true\n")

        # Case 2: No Changes (False)
        mock_workflow.return_value.run.return_value = False
        with patch.object(sys, "argv", ["issue-kit"] + test_args):
            cli.main()

        mock_file().write.assert_called_with("has_changes=false\n")
