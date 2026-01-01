# ruff: noqa: T201
import argparse
import os
import shutil
import sys
from pathlib import Path

from issue_creator_kit.scripts import create_issues, process_approvals

PACKAGE_ROOT = Path(__file__).parent
ASSETS_DIR = PACKAGE_ROOT / "assets"


def init_project(args):
    """Deploy workflows and templates to the current directory."""
    print("Initializing Issue Creator Kit...")

    # Define targets
    targets = {
        ASSETS_DIR / "workflows": Path(".github/workflows"),
        ASSETS_DIR / "templates": Path("reqs/template"),
    }

    for src_dir, dst_dir in targets.items():
        if not src_dir.exists():
            print(f"Error: Asset directory not found: {src_dir}")
            continue

        if not dst_dir.exists():
            dst_dir.mkdir(parents=True, exist_ok=True)
            print(f"Created directory: {dst_dir}")

        for item in src_dir.glob("*"):
            if item.is_file():
                dst_file = dst_dir / item.name
                if dst_file.exists() and not args.force:
                    print(
                        f"Skipping existing file: {dst_file} (use --force to overwrite)"
                    )
                else:
                    shutil.copy2(item, dst_file)
                    print(f"Deployed: {dst_file}")

    # Also deploy the runner script itself?
    # Ideally, if installed via pip, the workflow should use the installed command.
    # But GitHub Actions environment might need a setup.
    # For now, we assume the user installs this package in the workflow.
    print("\nInitialization complete.")
    print("Please ensure your workflow installs this package:")
    print("  pip install git+https://github.com/your-org/issue_creator_kit.git")


def run_automation(args):
    """Run the issue creation automation."""
    print("Running issue automation...")
    # Delegate to the logic in create_issues.py
    # We need to make sure create_issues.py exposes a main function or logic we can call.
    try:
        create_issues.main()
    except Exception as e:
        print(f"Automation failed: {e}")
        sys.exit(1)


def approve_document(args):
    """Run the approval process."""
    repo = args.repo or os.environ.get("GITHUB_REPOSITORY")
    token = args.token or os.environ.get("GITHUB_TOKEN")

    if not repo:
        print(
            "Error: Repository not specified. Use --repo or set GITHUB_REPOSITORY.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not token:
        print(
            "Error: Token not specified. Use --token or set GITHUB_TOKEN.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Approving document: {args.file_path}")
    try:
        process_approvals.process_single_file(
            file_path=args.file_path,
            approved_dir=args.approved_dir,
            repo_name=repo,
            token=token,
        )
    except Exception as e:
        print(f"Approval process failed: {e}", file=sys.stderr)
        sys.exit(1)


def approve_all_documents(args):
    """Run the batch approval process for all files in inbox."""
    repo = args.repo or os.environ.get("GITHUB_REPOSITORY")
    token = args.token or os.environ.get("GITHUB_TOKEN")

    if not repo:
        print(
            "Error: Repository not specified. Use --repo or set GITHUB_REPOSITORY.",
            file=sys.stderr,
        )
        sys.exit(1)
    if not token:
        print(
            "Error: Token not specified. Use --token or set GITHUB_TOKEN.",
            file=sys.stderr,
        )
        sys.exit(1)

    print(f"Approving all documents in: {args.inbox_dir}")
    try:
        processed = process_approvals.process_all_files(
            inbox_dir=args.inbox_dir,
            approved_dir=args.approved_dir,
            repo_name=repo,
            token=token,
        )
        if not processed:
            print("No documents processed.")
            # This is not necessarily an error for the CLI, but we might want to signal it.
            # For now, exit 0 is fine.
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

    # run command (for CI usage)
    # Assigning to a variable to avoid F841 if not used, or just don't assign.
    subparsers.add_parser("run", help="Run the issue creation automation")

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
    elif args.command == "run":
        run_automation(args)
    elif args.command == "approve":
        approve_document(args)
    elif args.command == "approve-all":
        approve_all_documents(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
