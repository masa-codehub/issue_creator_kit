# ruff: noqa: T201
import argparse
import re
import shutil
import sys
from pathlib import Path

from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter
from issue_creator_kit.usecase.creation import IssueCreationUseCase
from issue_creator_kit.usecase.roadmap_sync import RoadmapSyncUseCase

PACKAGE_ROOT = Path(__file__).parent
PROJECT_TEMPLATE_DIR = PACKAGE_ROOT / "assets" / "project_template"

# Constants
ADR_ID_PATTERN = r"^adr-\d{3}$"


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


def adr_id_type(value: str) -> str:
    """Validate ADR ID format (adr-XXX)."""
    if not re.match(ADR_ID_PATTERN, value):
        raise argparse.ArgumentTypeError(
            f"Invalid --adr-id format: {value}. Expected adr-XXX (e.g., adr-001)."
        )
    return value


def run_automation(args):
    """Run the issue creation automation (Virtual Queue)."""
    print("Running issue automation (Virtual Queue)...")

    fs = FileSystemAdapter()
    gh = GitHubAdapter(repo=args.repo, token=args.token)
    git = GitAdapter()
    roadmap_sync = RoadmapSyncUseCase(fs)

    usecase = IssueCreationUseCase(fs, gh, git_adapter=git, roadmap_sync=roadmap_sync)

    try:
        # ADR-007 compliant UseCase call
        usecase.create_issues(
            before=args.before,
            after=args.after,
            adr_id=args.adr_id,
            archive_path=args.archive_dir,
            roadmap_path=args.roadmap,
            use_pr=args.use_pr,
            base_branch=args.base_branch,
        )
    except Exception as e:
        print(f"Automation failed: {e}", file=sys.stderr)
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
        "--adr-id",
        type=adr_id_type,
        help="ADR ID to filter tasks (format: adr-XXX)",
    )
    diff_parser.add_argument(
        "--archive-dir",
        default="reqs/tasks/_archive/",
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

    args = parser.parse_args()

    if args.command == "init":
        init_project(args)
    elif args.command == "process-diff":
        run_automation(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
