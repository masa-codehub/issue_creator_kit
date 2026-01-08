# ruff: noqa: T201
import argparse
import os
import shutil
import sys
from pathlib import Path

from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter
from issue_creator_kit.usecase.approval import ApprovalUseCase
from issue_creator_kit.usecase.creation import IssueCreationUseCase
from issue_creator_kit.usecase.roadmap_sync import RoadmapSyncUseCase
from issue_creator_kit.usecase.workflow import WorkflowUseCase

PACKAGE_ROOT = Path(__file__).parent
PROJECT_TEMPLATE_DIR = PACKAGE_ROOT / "assets" / "project_template"


def init_project(args):
    """Deploy project template to the current directory."""
    print("Initializing Issue Creator Kit Project...")

    if not PROJECT_TEMPLATE_DIR.exists():
        print(
            f"Error: Project template not found at {PROJECT_TEMPLATE_DIR}",
            file=sys.stderr,
        )
        sys.exit(1)

    # Recursive copy
    for item in PROJECT_TEMPLATE_DIR.glob("**/*"):
        if item.is_file():
            rel_path = item.relative_to(PROJECT_TEMPLATE_DIR)
            dst_path = Path.cwd() / rel_path

            if dst_path.exists() and not args.force:
                print(f"Skipping existing file: {rel_path} (use --force to overwrite)")
            else:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_path)
                print(f"Created: {rel_path}")

    print("\nInitialization complete.")


def run_automation(args):
    """Run the issue creation automation (Virtual Queue)."""
    print("Running issue automation (Virtual Queue)...")

    fs = FileSystemAdapter()
    gh = GitHubAdapter(repo=args.repo, token=args.token)
    git = GitAdapter()
    roadmap_sync = RoadmapSyncUseCase(fs)

    # Initialize ApprovalUseCase for WorkflowUseCase
    approval_usecase = ApprovalUseCase(fs, gh)
    workflow = WorkflowUseCase(
        approval_usecase=approval_usecase, git_adapter=git, github_adapter=gh
    )
    usecase = IssueCreationUseCase(
        fs, gh, git_adapter=git, roadmap_sync=roadmap_sync, workflow_usecase=workflow
    )

    try:
        usecase.create_issues_from_virtual_queue(
            base_ref=args.before,
            head_ref=args.after,
            archive_path=args.archive_dir,
            roadmap_path=args.roadmap,
            use_pr=args.use_pr,
            base_branch=args.base_branch,
        )
    except Exception as e:
        print(f"Automation failed: {e}", file=sys.stderr)
        sys.exit(1)


def run_merge_workflow(args):
    """Run the merge-triggered workflow (Auto-PR)."""
    print("Running merge-triggered workflow (Auto-PR)...")

    fs = FileSystemAdapter()
    gh = GitHubAdapter(repo=args.repo, token=args.token)
    git = GitAdapter()
    workflow = WorkflowUseCase(
        approval_usecase=None,
        git_adapter=git,
        github_adapter=gh,
        filesystem_adapter=fs,
    )

    try:
        workflow.promote_from_merged_pr(args.pr_body, archive_dir=args.archive_dir)
    except Exception as e:
        print(f"Merge workflow failed: {e}", file=sys.stderr)
        sys.exit(1)


def run_workflow(args):
    """Run the approval workflow (orchestration)."""
    # Initialize dependencies
    fs = FileSystemAdapter()
    gh = GitHubAdapter(repo=args.repo, token=args.token)
    approval_usecase = ApprovalUseCase(fs, gh)
    git_adapter = GitAdapter()
    workflow = WorkflowUseCase(approval_usecase, git_adapter)

    print(f"Running workflow... Branch: {args.branch}")
    try:
        changed = workflow.run(
            inbox_dir=args.inbox_dir,
            approved_dir=args.approved_dir,
            branch_name=args.branch,
        )
        if changed:
            print(f"Workflow completed. Changes pushed to {args.branch}.")
            if "GITHUB_OUTPUT" in os.environ:
                with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                    f.write("has_changes=true\n")
        else:
            print("No changes to process.")
            if "GITHUB_OUTPUT" in os.environ:
                with open(os.environ["GITHUB_OUTPUT"], "a") as f:
                    f.write("has_changes=false\n")
    except Exception as e:
        print(f"Workflow failed: {e}", file=sys.stderr)
        sys.exit(1)


def approve_document(args):
    """Run the approval process for a single file."""
    fs = FileSystemAdapter()
    gh = GitHubAdapter(repo=args.repo, token=args.token)
    usecase = ApprovalUseCase(fs, gh)

    print(f"Approving document: {args.file_path}")
    try:
        usecase.process_single_file(
            file_path=args.file_path, approved_dir=args.approved_dir
        )
    except Exception as e:
        print(f"Approval process failed: {e}", file=sys.stderr)
        sys.exit(1)


def approve_all_documents(args):
    """Run the batch approval process."""
    fs = FileSystemAdapter()
    gh = GitHubAdapter(repo=args.repo, token=args.token)
    usecase = ApprovalUseCase(fs, gh)

    print(f"Approving all documents in: {args.inbox_dir}")
    try:
        processed = usecase.process_all_files(
            inbox_dir=args.inbox_dir, approved_dir=args.approved_dir
        )
        if not processed:
            print("No documents processed.")
    except Exception as e:
        print(f"Batch approval process failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Issue Creator Kit CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize configuration in the current project"
    )
    init_parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing files"
    )

    # process-diff command (virtual queue)
    diff_parser = subparsers.add_parser(
        "process-diff", help="Run the issue creation automation from git diff"
    )
    diff_parser.add_argument(
        "--before", required=True, help="Base ref/SHA for comparison"
    )
    diff_parser.add_argument(
        "--after", required=True, help="Head ref/SHA for comparison"
    )
    diff_parser.add_argument(
        "--archive-dir",
        default="reqs/tasks/archive/",
        help="Directory to check for added task files",
    )
    diff_parser.add_argument(
        "--roadmap",
        help="Path to the roadmap file to synchronize",
    )
    diff_parser.add_argument(
        "--use-pr",
        action="store_true",
        help="Create a PR for metadata updates instead of pushing directly to main",
    )
    diff_parser.add_argument(
        "--base-branch",
        default="main",
        help="Base branch for the metadata sync PR (default: main)",
    )
    diff_parser.add_argument(
        "--repo",
        help="GitHub repository (owner/repo). Defaults to GITHUB_REPOSITORY if not set.",
    )
    diff_parser.add_argument(
        "--token",
        help="GitHub token. Defaults to GITHUB_TOKEN if not set.",
    )

    # process-merge command
    merge_parser = subparsers.add_parser(
        "process-merge", help="Run the Auto-PR logic triggered by a merged PR"
    )
    merge_parser.add_argument(
        "--pr-body", required=True, help="Body of the merged Pull Request"
    )
    merge_parser.add_argument(
        "--archive-dir",
        default="reqs/tasks/archive",
        help="Directory to check for completed task files",
    )
    merge_parser.add_argument(
        "--repo",
        required=True,
        help="GitHub repository (owner/repo).",
    )
    merge_parser.add_argument(
        "--token",
        required=True,
        help="GitHub token.",
    )

    # run-workflow command
    workflow_parser = subparsers.add_parser(
        "run-workflow", help="Run the approval workflow orchestration"
    )
    workflow_parser.add_argument(
        "--inbox-dir",
        type=Path,
        default=Path("reqs/design/_inbox"),
        help="Directory containing documents to process",
    )
    workflow_parser.add_argument(
        "--approved-dir",
        type=Path,
        default=Path("reqs/design/_approved"),
        help="Directory to move approved files to",
    )
    workflow_parser.add_argument(
        "--branch",
        required=True,
        help="Target branch to push changes to",
    )
    workflow_parser.add_argument(
        "--repo",
        help="GitHub repository (owner/repo).",
    )
    workflow_parser.add_argument(
        "--token",
        help="GitHub token.",
    )

    # approve command
    approve_parser = subparsers.add_parser(
        "approve", help="Process an approved document"
    )
    approve_parser.add_argument(
        "file_path", type=Path, help="Path to the document to approve"
    )
    approve_parser.add_argument(
        "--repo",
        help="GitHub repository (owner/repo). Defaults to GITHUB_REPOSITORY env var.",
    )
    approve_parser.add_argument(
        "--token", help="GitHub token. Defaults to GITHUB_TOKEN env var."
    )
    approve_parser.add_argument(
        "--approved-dir",
        type=Path,
        default=Path("reqs/design/_approved"),
        help="Directory to move approved files to",
    )

    # approve-all command
    approve_all_parser = subparsers.add_parser(
        "approve-all", help="Process all approved documents in inbox"
    )
    approve_all_parser.add_argument(
        "--inbox-dir",
        type=Path,
        default=Path("reqs/design/_inbox"),
        help="Directory containing approved documents",
    )
    approve_all_parser.add_argument(
        "--repo",
        help="GitHub repository (owner/repo). Defaults to GITHUB_REPOSITORY env var.",
    )
    approve_all_parser.add_argument(
        "--token", help="GitHub token. Defaults to GITHUB_TOKEN env var."
    )
    approve_all_parser.add_argument(
        "--approved-dir",
        type=Path,
        default=Path("reqs/design/_approved"),
        help="Directory to move approved files to",
    )

    args = parser.parse_args()

    if args.command == "init":
        init_project(args)
    elif args.command == "process-diff":
        run_automation(args)
    elif args.command == "process-merge":
        run_merge_workflow(args)
    elif args.command == "run-workflow":
        run_workflow(args)
    elif args.command == "approve":
        approve_document(args)
    elif args.command == "approve-all":
        approve_all_documents(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
