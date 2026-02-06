# ruff: noqa: T201
import re
from pathlib import Path

from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter
from issue_creator_kit.usecase.approval import ApprovalUseCase


class WorkflowUseCase:
    """
    UseCase for managing the end-to-end task workflow, including document approvals
    and automatic phase promotion (Auto-PR).
    """

    MAX_PHASE_CHAIN_DEPTH = 10

    def __init__(
        self,
        approval_usecase: ApprovalUseCase | None,
        git_adapter: GitAdapter,
        github_adapter: GitHubAdapter | None = None,
        filesystem_adapter: FileSystemAdapter | None = None,
    ):
        self.approval_usecase = approval_usecase
        self.git_adapter = git_adapter
        self.github_adapter = github_adapter
        self.fs = filesystem_adapter or FileSystemAdapter()
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

        Error Handling Strategy:
        - Catch specific branch-exists errors to skip silently (idempotent).
        - Propagate other fatal git/network errors to avoid inconsistent state.
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

        # Derive and validate phase name
        p = Path(next_phase_path)
        candidate = p.name
        if not candidate:
            parent = p.parent
            if parent and parent != p:
                candidate = parent.name

        phase_name = candidate.strip() if candidate else ""
        if not phase_name:
            print(
                f"Warning: Could not derive valid phase name from {next_phase_path}. Skipping."
            )
            return

        new_branch = f"feature/{phase_name}-foundation"

        # Derive destination: replace only the 'drafts' segment with 'archive'
        if "drafts" in p.parts:
            replaced_parts = [
                "archive" if part == "drafts" else part for part in p.parts
            ]
            dest_path = str(Path(*replaced_parts))
        else:
            print(
                f"Warning: 'drafts' segment not found in path {next_phase_path}. Skipping promotion."
            )
            return

        if Path(dest_path).exists():
            print(
                f"Warning: Destination {dest_path} already exists. Skipping promotion."
            )
            return

        try:
            print(f"Promoting to next phase: {phase_name}")
            # 1. Create foundation branch
            try:
                self.git_adapter.checkout(new_branch, create=True, base="main")
            except RuntimeError as e:
                # Handle cases where branch already exists specifically
                if "already exists" in str(e):
                    print(
                        f"Warning: Branch {new_branch} already exists. Skipping promotion."
                    )
                    return
                raise

            # 2. Move files
            self.git_adapter.move_file(next_phase_path, dest_path.rstrip("/"))

            # 3. Commit and Push
            self.git_adapter.commit(
                f"feat: promote {phase_name} tasks for virtual queue"
            )
            self.git_adapter.push(remote="origin", branch=new_branch, set_upstream=True)

            # 4. Create PR
            if self.github_adapter:
                title = f"feat: promote {phase_name} tasks"
                body = f"Automatic promotion of tasks for {phase_name} from drafts to archive."
                pr_url, pr_number = self.github_adapter.create_pull_request(
                    title, body, head=new_branch, base="main"
                )
                print(f"Successfully created PR #{pr_number}: {pr_url}")

        except Exception as e:
            # For git mv, commit, push, or PR creation, failures are logged and propagated
            # to ensure the process stops and maintains repo consistency.
            print(f"Critical: Error during phase promotion for {phase_name}: {e}")
            raise

    def promote_from_merged_pr(
        self, pr_body: str, archive_dir: str = "reqs/tasks/archive"
    ) -> None:
        """
        Analyzes a merged PR body to find linked issues and promote to the next phase
         if the task file contains a next_phase_path.
        """
        if not pr_body:
            return

        # Reset state for a fresh promotion chain
        self.visited_phase_paths = set()
        self.phase_chain_depth = 0

        # 1. Extract issue numbers using regex
        # Matches keywords like Closes, Fixes, Resolves followed by #number (whitespace optional)
        pattern = r"(?i)(?:close|closes|closed|fix|fixes|fixed|resolve|resolves|resolved)\s*#(\d+)"
        issue_numbers = re.findall(pattern, pr_body)

        if not issue_numbers:
            return

        print(f"Detected linked issues in PR body: {issue_numbers}")

        # 2. Scan archive/ to find matching task files and build a lookup map (O(N+M))
        archive_path = Path(archive_dir)
        all_task_files = self.fs.list_files(archive_path, pattern="**/*.md")

        issue_to_phase_map: dict[str, str] = {}
        for task_file in all_task_files:
            try:
                doc = self.fs.read_document(task_file)
                issue = doc.metadata.get("issue")
                next_phase = doc.metadata.get("next_phase_path")
                if issue and next_phase:
                    # Assumes issue format is '#123'
                    issue_number_str = str(issue).lstrip("#")
                    issue_to_phase_map[issue_number_str] = next_phase
            except (FileNotFoundError, PermissionError) as e:
                # Fatal: Cannot proceed if we can't access files we know exist
                print(f"Critical Error: Failed to access task file {task_file}: {e}")
                raise
            except Exception as e:
                # Non-fatal: Skip malformed files but log warning
                print(f"Warning: Failed to parse task file {task_file}: {e}")
                continue
        # 3. Process all promotable tasks found in the PR's issues
        promoted_count = 0
        errors = []
        for issue_no in issue_numbers:
            if issue_no in issue_to_phase_map:
                next_phase = issue_to_phase_map[issue_no]
                print(
                    f"Detected merged PR for Issue #{issue_no}. Next phase found: {next_phase}"
                )
                try:
                    self.promote_next_phase(next_phase)
                    promoted_count += 1
                except Exception as e:
                    error_msg = f"Error promoting phase for Issue #{issue_no}: {e}"
                    print(error_msg)
                    errors.append(error_msg)

        if errors:
            raise RuntimeError(
                f"One or more phase promotions failed: {'; '.join(errors)}"
            )

        if promoted_count == 0:
            print("No next_phase_path found for the linked issues.")
        else:
            print(f"Successfully triggered {promoted_count} phase promotions.")
