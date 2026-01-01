import unittest
from pathlib import Path
from unittest.mock import MagicMock

from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.usecase.approval import ApprovalUseCase
from issue_creator_kit.usecase.workflow import WorkflowUseCase


class TestWorkflowUseCase(unittest.TestCase):
    def setUp(self):
        self.mock_approval_usecase = MagicMock(spec=ApprovalUseCase)
        self.mock_git_adapter = MagicMock(spec=GitAdapter)
        self.workflow = WorkflowUseCase(
            self.mock_approval_usecase, self.mock_git_adapter
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
        # Verify GitAdapter methods were NOT called
        # Note: checkout might be called depending on implementation logic (prepare branch first or after?)
        # If we prepare branch first, checkout would be called.
        # If we optimize to only prepare if needed, it wouldn't.
        # Let's assume we prepare branch first to be safe for file ops?
        # Actually, file ops are local. If we move files, we change workspace.
        # Better to be on the target branch BEFORE moving files to avoid carrying changes over if we switch later.
        self.mock_git_adapter.checkout.assert_called_once_with(
            self.branch_name, create=True
        )

        # But commit/push should not be called
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
        # Verify GitAdapter workflow
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

        # Verify no commit/push happened
        self.mock_git_adapter.commit.assert_not_called()
        self.mock_git_adapter.push.assert_not_called()
