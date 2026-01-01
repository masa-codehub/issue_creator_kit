from pathlib import Path
from unittest.mock import Mock

import pytest

from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.usecase.approval import ApprovalUseCase
from issue_creator_kit.usecase.workflow import WorkflowUseCase


class TestWorkflowUseCase:
    @pytest.fixture
    def mocks(self):
        approval_usecase = Mock(spec=ApprovalUseCase)
        git_adapter = Mock(spec=GitAdapter)
        return approval_usecase, git_adapter

    def test_run_success(self, mocks):
        """
        Given: ApprovalUseCase returns True (files processed)
        When: run is called
        Then: Git operations (checkout, add, commit, push) are executed
        """
        approval_usecase, git_adapter = mocks
        workflow = WorkflowUseCase(approval_usecase, git_adapter)

        approval_usecase.process_all_files.return_value = True

        inbox_dir = Path("inbox")
        approved_dir = Path("approved")
        branch_name = "test-branch"

        result = workflow.run(inbox_dir, approved_dir, branch_name)

        assert result is True
        git_adapter.checkout.assert_called_once_with(branch_name, create=True)
        approval_usecase.process_all_files.assert_called_once_with(
            inbox_dir, approved_dir
        )
        git_adapter.add.assert_called_once_with(["."])
        git_adapter.commit.assert_called_once()
        git_adapter.push.assert_called_once_with(branch=branch_name, set_upstream=True)

    def test_run_no_changes(self, mocks):
        """
        Given: ApprovalUseCase returns False (no files processed)
        When: run is called
        Then: Only checkout is called, NO commit/push
        """
        approval_usecase, git_adapter = mocks
        workflow = WorkflowUseCase(approval_usecase, git_adapter)

        approval_usecase.process_all_files.return_value = False

        inbox_dir = Path("inbox")
        approved_dir = Path("approved")
        branch_name = "test-branch"

        result = workflow.run(inbox_dir, approved_dir, branch_name)

        assert result is False
        git_adapter.checkout.assert_called_once_with(branch_name, create=True)
        approval_usecase.process_all_files.assert_called_once_with(
            inbox_dir, approved_dir
        )

        git_adapter.add.assert_not_called()
        git_adapter.commit.assert_not_called()
        git_adapter.push.assert_not_called()

    def test_run_error(self, mocks):
        """
        Given: ApprovalUseCase raises Exception
        When: run is called
        Then: Exception is propagated
        """
        approval_usecase, git_adapter = mocks
        workflow = WorkflowUseCase(approval_usecase, git_adapter)

        approval_usecase.process_all_files.side_effect = RuntimeError(
            "Processing failed"
        )

        inbox_dir = Path("inbox")
        approved_dir = Path("approved")
        branch_name = "test-branch"

        with pytest.raises(RuntimeError, match="Processing failed"):
            workflow.run(inbox_dir, approved_dir, branch_name)

        git_adapter.checkout.assert_called_once()
        git_adapter.commit.assert_not_called()
