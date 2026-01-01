from pathlib import Path

from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.usecase.approval import ApprovalUseCase


class WorkflowUseCase:
    def __init__(self, approval_usecase: ApprovalUseCase, git_adapter: GitAdapter):
        self.approval_usecase = approval_usecase
        self.git_adapter = git_adapter

    def run(self, inbox_dir: Path, approved_dir: Path, branch_name: str) -> bool:
        """
        Runs the approval workflow:
        1. Checkout/Create target branch.
        2. Process approvals.
        3. If changes, commit and push.
        """
        # 1. Prepare branch
        self.git_adapter.checkout(branch_name, create=True)

        # 2. Process files
        processed = self.approval_usecase.process_all_files(inbox_dir, approved_dir)

        if processed:
            # 3. Commit and Push
            self.git_adapter.add(["."])
            self.git_adapter.commit("feat: process approved documents")
            self.git_adapter.push(branch=branch_name, set_upstream=True)
            return True

        return False
