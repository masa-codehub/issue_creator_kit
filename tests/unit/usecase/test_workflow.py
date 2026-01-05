import unittest
from pathlib import Path
from unittest.mock import MagicMock

from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter
from issue_creator_kit.usecase.approval import ApprovalUseCase
from issue_creator_kit.usecase.workflow import WorkflowUseCase


class TestWorkflowUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_approval_usecase = MagicMock(spec=ApprovalUseCase)
        self.mock_git_adapter = MagicMock(spec=GitAdapter)
        self.mock_github_adapter = MagicMock(spec=GitHubAdapter)
        self.workflow = WorkflowUseCase(
            self.mock_approval_usecase,
            self.mock_git_adapter,
            github_adapter=self.mock_github_adapter,
        )
        self.inbox_dir = Path("reqs/design/_inbox")
        self.approved_dir = Path("reqs/design/_approved")
        self.branch_name = "test-branch"

    def test_run_no_files_processed(self):
        # Given: ApprovalUseCase returns False (no files processed)
        self.mock_approval_usecase.process_all_files.return_value = False

        # When
        result = self.workflow.run(self.inbox_dir, self.approved_dir, self.branch_name)

        # Then
        self.assertFalse(result)
        self.mock_git_adapter.checkout.assert_called_once_with(
            self.branch_name, create=True
        )
        self.mock_git_adapter.add.assert_not_called()
        self.mock_git_adapter.commit.assert_not_called()
        self.mock_git_adapter.push.assert_not_called()

    def test_run_files_processed_and_changes_pushed(self):
        # Given: ApprovalUseCase returns True (files processed)
        self.mock_approval_usecase.process_all_files.return_value = True

        # When
        result = self.workflow.run(self.inbox_dir, self.approved_dir, self.branch_name)

        # Then
        self.assertTrue(result)
        self.mock_git_adapter.checkout.assert_called_once_with(
            self.branch_name, create=True
        )
        self.mock_approval_usecase.process_all_files.assert_called_once_with(
            self.inbox_dir, self.approved_dir
        )
        self.mock_git_adapter.add.assert_called_once_with(["."])
        self.mock_git_adapter.commit.assert_called_once_with(
            "docs: approve documents and create tracking issues"
        )
        self.mock_git_adapter.push.assert_called_once_with(
            branch=self.branch_name, set_upstream=True
        )

    def test_run_error_propagates(self):
        # Given: ApprovalUseCase raises an exception
        self.mock_approval_usecase.process_all_files.side_effect = RuntimeError(
            "Processing failed"
        )

        # When/Then
        with self.assertRaises(RuntimeError):
            self.workflow.run(self.inbox_dir, self.approved_dir, self.branch_name)

        self.mock_git_adapter.commit.assert_not_called()
        self.mock_git_adapter.push.assert_not_called()

    def test_promote_next_phase_success(self):
        # Setup
        next_phase_path = "reqs/tasks/drafts/phase-2/"
        expected_dest = "reqs/tasks/archive/phase-2/"

        # Execute
        self.workflow.promote_next_phase(next_phase_path)

        # Verify Git operations
        self.mock_git_adapter.checkout.assert_called_with(
            "feature/phase-2-foundation", create=True, base="main"
        )
        self.mock_git_adapter.move_file.assert_called_with(
            next_phase_path, expected_dest
        )
        self.mock_git_adapter.commit.assert_called()
        self.mock_git_adapter.push.assert_called_with(
            remote="origin", branch="feature/phase-2-foundation", set_upstream=True
        )

        # Verify GitHub operations
        self.mock_github_adapter.create_pull_request.assert_called_once()
        args, kwargs = self.mock_github_adapter.create_pull_request.call_args
        title = kwargs.get("title", args[0]) if args else kwargs.get("title")
        self.assertIn("phase-2", title)
        self.assertEqual(kwargs.get("head"), "feature/phase-2-foundation")
        self.assertEqual(kwargs.get("base"), "main")

    def test_promote_next_phase_skips_if_branch_exists(self):
        # Setup
        next_phase_path = "reqs/tasks/drafts/phase-2/"
        self.mock_git_adapter.checkout.side_effect = RuntimeError(
            "Git command failed: fatal: A branch named 'feature/phase-2-foundation' already exists."
        )

        # Execute
        self.workflow.promote_next_phase(next_phase_path)

        # Verify PR was NOT created
        self.mock_github_adapter.create_pull_request.assert_not_called()

    def test_promote_next_phase_circular_dependency(self):
        # Setup
        path1 = "reqs/tasks/drafts/phase-1/"
        self.workflow.visited_phase_paths.add(path1)

        # Execute with path1 again
        self.workflow.promote_next_phase(path1)

        # Verify no action taken
        self.mock_git_adapter.checkout.assert_not_called()

    def test_promote_next_phase_max_depth(self):
        # Setup
        self.workflow.phase_chain_depth = 10

        # Execute
        self.workflow.promote_next_phase("reqs/tasks/drafts/phase-11/")

        # Verify no action taken
        self.mock_git_adapter.checkout.assert_not_called()
