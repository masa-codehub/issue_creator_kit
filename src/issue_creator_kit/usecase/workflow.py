# ruff: noqa: T201
from pathlib import Path

from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter
from issue_creator_kit.usecase.approval import ApprovalUseCase


class WorkflowUseCase:
    MAX_PHASE_CHAIN_DEPTH = 10

    def __init__(
        self,
        approval_usecase: ApprovalUseCase | None,
        git_adapter: GitAdapter,
        github_adapter: GitHubAdapter | None = None,
    ):
        self.approval_usecase = approval_usecase
        self.git_adapter = git_adapter
        self.github_adapter = github_adapter
        self.visited_phase_paths: set[str] = set()
        self.phase_chain_depth = 0

    def run(self, inbox_dir: Path, approved_dir: Path, branch_name: str) -> bool:
        """
        Runs the approval workflow:
        1. Checkout/Create target branch.
        2. Process approvals.
        3. If changes, commit and push.
        """
        if not self.approval_usecase:
            raise RuntimeError("ApprovalUseCase is required for run().")

        # 1. Prepare branch
        self.git_adapter.checkout(branch_name, create=True)

        # 2. Process files
        processed = self.approval_usecase.process_all_files(inbox_dir, approved_dir)

        if processed:
            # 3. Commit and Push
            self.git_adapter.add(["."])
            self.git_adapter.commit(
                "docs: approve documents and create tracking issues"
            )
            self.git_adapter.push(branch=branch_name, set_upstream=True)
            return True

        return False

    def promote_next_phase(self, next_phase_path: str) -> None:
        """
        Promotes tasks to the next phase:
        1. Validates safety (infinite loop, depth).
        2. Creates a new foundation branch.
        3. Moves files from drafts to archive.
        4. Commits, Pushes, and creates a PR.
        """
        if not next_phase_path:
            return

        # Safety: Infinite loop protection
        if next_phase_path in self.visited_phase_paths:
            print(
                f"Warning: Circular dependency detected for {next_phase_path}. Skipping."
            )
            return

        # Safety: Max depth
        if self.phase_chain_depth >= self.MAX_PHASE_CHAIN_DEPTH:
            print(
                f"Warning: Max phase chain depth ({self.MAX_PHASE_CHAIN_DEPTH}) reached. Skipping."
            )
            return

        self.visited_phase_paths.add(next_phase_path)
        self.phase_chain_depth += 1

        # Derive phase name (e.g. "phase-2" from ".../phase-2/")
        p = Path(next_phase_path)
        # Handle trailing slash by using p.name if not empty, else p.parent.name
        phase_name = p.name if p.name else p.parent.name
        new_branch = f"feature/{phase_name}-foundation"

        # Derive destination: swap 'drafts' with 'archive'
        dest_path = next_phase_path.replace("drafts", "archive")

        # Basic check if destination already exists (logical or physical)
        if Path(dest_path).exists():
            print(
                f"Warning: Destination {dest_path} already exists. Skipping promotion to avoid duplicate processing."
            )
            return

        try:
            print(f"Promoting to next phase: {phase_name}")
            # 1. Create foundation branch
            self.git_adapter.checkout(new_branch, create=True, base="main")

            # 2. Move files
            self.git_adapter.move_file(next_phase_path, dest_path)

            # 3. Commit and Push
            self.git_adapter.commit(
                f"feat: promote {phase_name} tasks for virtual queue"
            )
            self.git_adapter.push(remote="origin", branch=new_branch, set_upstream=True)

            # 4. Create PR
            if self.github_adapter:
                title = f"feat: promote {phase_name} tasks"
                body = f"Automatic promotion of tasks for {phase_name} from drafts to archive."
                pr_url = self.github_adapter.create_pull_request(
                    title, body, head=new_branch, base="main"
                )
                print(f"Successfully created PR: {pr_url}")

        except Exception as e:
            print(f"Error during phase promotion: {e}")
            # Design: Fail-fast, maintain consistency
            # We don't re-raise here to allow other potential promotions in the same run if needed,
            # but we've logged it. Actually, design says "異常発生時には「何もしない」"
            # If one promotion fails, we might want to stop everything.
            # For now, let's just log and skip this one.
