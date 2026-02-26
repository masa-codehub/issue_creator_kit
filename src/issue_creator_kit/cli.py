# ruff: noqa: T201
import argparse
import json
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

from pydantic import ValidationError

from issue_creator_kit.domain.exceptions import (
    DomainError,
    SecurityValidationError,
)
from issue_creator_kit.domain.models.config import IssueKitConfig
from issue_creator_kit.domain.services.builder import GraphBuilder
from issue_creator_kit.domain.services.l1_sync import L1SyncService
from issue_creator_kit.domain.services.metadata_parser import MetadataParser
from issue_creator_kit.domain.services.parser import DocumentParser
from issue_creator_kit.domain.services.renderer import IssueRenderer
from issue_creator_kit.domain.services.scanner import FileSystemScanner
from issue_creator_kit.domain.services.visualizer import Visualizer
from issue_creator_kit.infrastructure.error_handler import (
    ICKErrorHandler,
    ValidationErrorData,
)
from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter
from issue_creator_kit.usecase.l1_automation_usecase import L1AutomationUseCase
from issue_creator_kit.usecase.orchestrator_service import OrchestratorService
from issue_creator_kit.usecase.relay_engine import RelayEngine
from issue_creator_kit.usecase.scanner_usecase import ScannerUseCase
from issue_creator_kit.usecase.task_activation_usecase import (
    TaskActivationUseCase,
)
from issue_creator_kit.usecase.validator import TaskGraphValidator

PACKAGE_ROOT = Path(__file__).parent
PROJECT_TEMPLATE_DIR = PACKAGE_ROOT / "assets" / "project_template"

# Constants
ADR_ID_PATTERN = r"^adr-\d{3}$"
SAFE_PATH_PATTERN = r"^[A-Za-z0-9/._-]+$"


def validate_path(path_str: str, param_name: str) -> None:
    """
    Validate path string against security constraints.
    - No '..'
    - No leading '/' or '\'
    - Whitelist: A-Za-z0-9/._-
    - No continuous slashes '//'
    - Must be within repository boundaries (logical check)
    - No URL encoded characters allowed in the input string
    """
    if not path_str or path_str.isspace():
        raise SecurityValidationError(f"Invalid path: {param_name} is empty or blank.")

    # URL Encoding check: Input must not contain encoded characters
    decoded_path = urllib.parse.unquote(path_str)
    if path_str != decoded_path:
        raise SecurityValidationError(
            f"Invalid path: {param_name} contains URL encoded characters."
        )

    # Basic string checks
    if ".." in decoded_path:
        raise SecurityValidationError(f"Invalid path: {param_name} contains '..'")

    if decoded_path.startswith("/") or decoded_path.startswith("\\"):
        raise SecurityValidationError(
            f"Invalid path: absolute path not allowed for {param_name}"
        )

    if "\\" in decoded_path:
        raise SecurityValidationError(
            f"Invalid path: backslashes not allowed for {param_name}"
        )

    if "//" in decoded_path:
        raise SecurityValidationError(
            f"Invalid path: continuous slashes not allowed for {param_name}"
        )

    # Whitelist check
    if not re.match(SAFE_PATH_PATTERN, decoded_path):
        raise SecurityValidationError(
            f"Invalid path: {param_name} contains invalid characters."
        )

    # Logical boundary check using resolve()
    try:
        # We assume the tool is running from the repository root
        base_dir = Path.cwd().resolve()
        target_path = (base_dir / decoded_path).resolve()

        if not target_path.is_relative_to(base_dir):
            raise SecurityValidationError(
                f"Invalid path: path must stay within repository boundaries for {param_name}"
            )
    except Exception as e:
        if isinstance(e, SecurityValidationError):
            raise
        raise SecurityValidationError(
            f"Invalid path: Could not resolve {param_name}: {e}"
        ) from e


def init_project(args):
    """Deploy project template to the current directory."""
    print("Initializing Issue Creator Kit Project...", file=sys.stderr)

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
                print(
                    f"Skipping existing file: {rel_path} (use --force to overwrite)",
                    file=sys.stderr,
                )
            else:
                dst_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dst_path)
                print(f"Created: {rel_path}", file=sys.stderr)

    print("\nInitialization complete.", file=sys.stderr)


def adr_id_type(value: str) -> str:
    """Validate ADR ID format (adr-XXX)."""
    if not re.match(ADR_ID_PATTERN, value):
        raise argparse.ArgumentTypeError(
            f"Invalid --adr-id format: {value}. Expected adr-XXX (e.g., adr-001)."
        )
    return value


def run_automation(args):
    """Run the issue creation automation (Virtual Queue)."""
    print(
        "Error: This command is deprecated and no longer supported. Use `issue-kit process` instead.",
        file=sys.stderr,
    )
    sys.exit(1)


def get_scanner_usecase():
    """Helper to instantiate ScannerUseCase with its dependencies."""
    parser = DocumentParser()
    scanner = FileSystemScanner(parser)
    builder = GraphBuilder()
    visualizer = Visualizer()
    return ScannerUseCase(scanner, builder, visualizer)


def get_l1_automation_usecase():
    """Helper to instantiate L1AutomationUseCase with its dependencies."""
    parser = DocumentParser()
    scanner = FileSystemScanner(parser)
    github = GitHubAdapter()
    return L1AutomationUseCase(scanner, github)


def get_task_activation_usecase():
    """Helper to instantiate TaskActivationUseCase with its dependencies."""
    parser = DocumentParser()
    scanner = FileSystemScanner(parser)
    builder = GraphBuilder()
    github = GitHubAdapter()
    fs = FileSystemAdapter()
    l1_sync = L1SyncService(github)
    renderer = IssueRenderer()
    return TaskActivationUseCase(scanner, builder, github, fs, l1_sync, renderer)


def get_orchestrator_service():
    """Helper to instantiate OrchestratorService with its dependencies."""
    parser = DocumentParser()
    scanner = FileSystemScanner(parser)
    github = GitHubAdapter()

    l1_usecase = L1AutomationUseCase(scanner, github)

    builder = GraphBuilder()
    fs = FileSystemAdapter()
    l1_sync = L1SyncService(github)
    renderer = IssueRenderer()
    task_usecase = TaskActivationUseCase(
        scanner, builder, github, fs, l1_sync, renderer
    )

    return OrchestratorService(l1_usecase, task_usecase, scanner, github)


def get_relay_engine():
    """Helper to instantiate RelayEngine with its dependencies."""
    github = GitHubAdapter()
    metadata_parser = MetadataParser()
    renderer = IssueRenderer()
    return RelayEngine(github, metadata_parser, renderer)


def _validate_execution_guards(args):
    """Ensure --execute or --dry-run is specified and they are mutually exclusive."""
    if not (args.execute or args.dry_run):
        print(
            "Error: Either --execute or --dry-run must be specified.",
            file=sys.stderr,
        )
        sys.exit(2)

    if args.execute and args.dry_run:
        print(
            "Error: --execute and --dry-run are mutually exclusive.",
            file=sys.stderr,
        )
        sys.exit(2)


def run_process(args):
    """Run the scanner and process ADRs/Tasks."""
    _validate_execution_guards(args)

    validate_path(args.root, "--root")
    if args.config_path:
        validate_path(args.config_path, "--config-path")

    root_path = Path(args.root)
    config = {}

    if args.config_path:
        config_file = Path(args.config_path)
        if not config_file.exists():
            print(
                f"エラー: 設定ファイルが見つかりません: {args.config_path}",
                file=sys.stderr,
            )
            sys.exit(1)
        try:
            with config_file.open() as f:
                config = json.load(f)
        except json.JSONDecodeError as e:
            print(f"エラー: JSON設定ファイルの解析に失敗しました: {e}", file=sys.stderr)
            sys.exit(1)
        except OSError as e:
            print(f"エラー: 設定ファイルの読み込みに失敗しました: {e}", file=sys.stderr)
            sys.exit(1)

    try:
        orchestrator = get_orchestrator_service()
        if args.execute:
            result = orchestrator.execute(root_path, dry_run=False, config=config)

            if result["l1_issue"] and result["new_l1"]:
                print(
                    f"[DONE] Created L1 Issue for {result['l1_adr_id']}. URL: {result['l1_url']}",
                    file=sys.stderr,
                )

            if result["l2_issues"]:
                print(
                    f"[DONE] Task activation complete. {len(result['l2_issues'])} tasks processed.",
                    file=sys.stderr,
                )

            if not result["success"]:
                failed_tasks = result.get("failed_tasks")
                if failed_tasks:
                    print(
                        f"[FAIL] {len(failed_tasks)} tasks failed: {failed_tasks}",
                        file=sys.stderr,
                    )
                sys.exit(1)
        else:
            # DRY-RUN path using Orchestrator
            result = orchestrator.execute(root_path, dry_run=True, config=config)

            # Also provide the document list preview as before (ADR-008/009 UX)
            usecase = get_scanner_usecase()
            scan_result = usecase.get_process_list(root_path)

            print(
                f"[INFO] Detected {len(scan_result.documents)} documents to process (execution order):",
                file=sys.stderr,
            )

            for doc in scan_result.documents:
                print(f"[INFO] - {doc.id}: {doc.title}", file=sys.stderr)

            # ADR-009 Dry-run summary
            print(
                f"\nDry-run summary: {len(scan_result.documents)} to be created, 0 skipped, 0 errors.",
                file=sys.stderr,
            )
            print("(Use --execute to actually create issues)", file=sys.stderr)

    except DomainError as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        sys.exit(1)

    except ValueError as e:
        # Handle configuration issues (missing tokens/repo) from GitHubAdapter

        print(
            "[FAIL] GitHub configuration issue. "
            "Please ensure GH_TOKEN or GITHUB_TOKEN, and GITHUB_REPOSITORY are set.",
            file=sys.stderr,
        )

        print(f"Details: {e}", file=sys.stderr)

        sys.exit(1)

    except Exception as e:
        print(f"[FAIL] Unexpected Error: {e}", file=sys.stderr)

        sys.exit(1)


def run_relay(args):
    """Run the relay engine for a specific issue."""
    _validate_execution_guards(args)

    engine = get_relay_engine()
    try:
        engine.execute_relay(args.issue_no, dry_run=args.dry_run)
        print(
            f"[DONE] Relay processing completed for Issue #{args.issue_no}.",
            file=sys.stderr,
        )
    except Exception as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        sys.exit(1)


def run_sync_relay(args):
    """Run the relay engine to sync all issues."""
    _validate_execution_guards(args)

    engine = get_relay_engine()
    try:
        results = engine.execute_sync(label=args.label, dry_run=args.dry_run)
        print("\nExecution summary:", file=sys.stderr)
        print(f"  Success: {results['success']}", file=sys.stderr)
        print(f"  Skipped: {results['skipped']}", file=sys.stderr)
        print(f"  Failed:  {results['failed']}", file=sys.stderr)
    except Exception as e:
        print(f"[FAIL] {e}", file=sys.stderr)
        sys.exit(1)


def run_check(args):
    """Run the TaskGraphValidator to check for errors."""
    validate_path(args.root, "--root")
    validator = TaskGraphValidator()
    handler = ICKErrorHandler()
    result = validator.validate(args.root)

    if result.valid:
        print("[DONE] No validation errors found.", file=sys.stderr)
        return

    # Print errors and determine exit code
    has_cycle = False
    for error in result.errors:
        if error.code == "CYCLE_DETECTED":
            has_cycle = True

        print(handler.format(error, no_color=args.no_color), file=sys.stderr)

    if has_cycle:
        sys.exit(2)
    else:
        sys.exit(1)


def run_visualize(args):
    """Run the scanner and generate Mermaid visualization."""
    validate_path(args.root, "--root")
    usecase = get_scanner_usecase()

    try:
        mermaid_str = usecase.visualize_graph(args.root)
        print(mermaid_str)
    except DomainError as e:
        print(f"Visualization failed (Domain Error): {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Visualization failed (Unexpected Error): {e}", file=sys.stderr)
        sys.exit(1)


def run_dispatch(args):
    """Determine the agent role based on PR labels and configuration."""
    if args.config_path:
        validate_path(args.config_path, "--config-path")

    config_path = Path(args.config_path or ".github/issue-kit-config.json")

    if not config_path.exists():
        print(
            f"[FAIL] {config_path}:0 (config): Configuration file not found.",
            file=sys.stderr,
        )
        sys.exit(1)

    try:
        with config_path.open() as f:
            data = json.load(f)
        config = IssueKitConfig(**data)
    except json.JSONDecodeError as e:
        print(
            f"[FAIL] {config_path}:0 (config): Failed to parse JSON config file: {e}",
            file=sys.stderr,
        )
        sys.exit(1)
    except ValidationError as e:
        print(
            f"[FAIL] {config_path}:0 (config): Invalid configuration format. {e}",
            file=sys.stderr,
        )
        sys.exit(1)
    except Exception as e:
        print(
            f"[FAIL] {config_path}:0 (config): Unexpected error reading config: {e}",
            file=sys.stderr,
        )
        sys.exit(1)

    if args.get_trigger:
        sys.stdout.write(f"{config.trigger_label}\n")
        sys.exit(0)

    if not args.labels:
        print(
            "[FAIL] --labels is required unless --get-trigger is used.", file=sys.stderr
        )
        sys.exit(1)

    labels = [label.strip() for label in args.labels.split(",") if label.strip()]
    matched_mapping = config.find_role(labels)

    if args.get_context:
        if matched_mapping and matched_mapping.context:
            sys.stdout.write(f"{matched_mapping.context}\n")
            sys.exit(0)
        else:
            print(
                f"[FAIL] {config_path}:0 (roles): No context file mapped for labels: {args.labels}.",
                file=sys.stderr,
            )
            sys.exit(1)

    role_name = matched_mapping.name if matched_mapping else config.default_role

    if role_name:
        # stdout purity: ONLY the role name
        sys.stdout.write(f"{role_name}\n")
        sys.exit(0)
    else:
        print(
            f"[FAIL] {config_path}:0 (roles): No matching role found for labels: {args.labels}.",
            file=sys.stderr,
        )
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Issue Creator Kit CLI")
    parser.add_argument(
        "--no-color", action="store_true", help="Disable ANSI color output"
    )
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # ... (rest of parser setup)

    # init command
    init_parser = subparsers.add_parser(
        "init", help="Initialize configuration in the current project"
    )
    init_parser.add_argument(
        "--force", "-f", action="store_true", help="Overwrite existing files"
    )

    # process command
    process_parser = subparsers.add_parser(
        "process", help="Scan physical file system and determine execution order"
    )
    process_parser.add_argument(
        "--root", default="reqs", help="Root directory to scan (default: reqs)"
    )
    process_parser.add_argument(
        "--config-path", help="Path to a JSON configuration file (optional)"
    )
    process_parser.add_argument(
        "--execute",
        action="store_true",
        help="Actually create GitHub issues (has side effects)",
    )
    process_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Display detected files and order without taking action",
    )

    # check command (Linter / Guardrail)
    check_parser = subparsers.add_parser(
        "check", help="Statically validate task files (ID consistency, cycles, etc.)"
    )
    check_parser.add_argument(
        "--root", default="reqs", help="Root directory to scan (default: reqs)"
    )

    # relay command
    relay_parser = subparsers.add_parser(
        "relay", help="Trigger descendant tasks when an issue is closed"
    )
    relay_parser.add_argument(
        "--issue-no", type=int, required=True, help="Number of the closed issue"
    )
    relay_parser.add_argument(
        "--execute", action="store_true", help="Actually update descendant issues"
    )
    relay_parser.add_argument(
        "--dry-run", action="store_true", help="Preview updates without execution"
    )

    # sync-relay command
    sync_relay_parser = subparsers.add_parser(
        "sync-relay", help="Bulk sync all issue states with dependencies"
    )
    sync_relay_parser.add_argument(
        "--label", default="task", help="Label to scan (default: task)"
    )
    sync_relay_parser.add_argument(
        "--execute", action="store_true", help="Actually update issues"
    )
    sync_relay_parser.add_argument(
        "--dry-run", action="store_true", help="Preview updates without execution"
    )

    # visualize command
    visualize_parser = subparsers.add_parser(
        "visualize", help="Visualize task dependencies in Mermaid format"
    )
    visualize_parser.add_argument(
        "--root", default="reqs", help="Root directory to scan (default: reqs)"
    )

    # dispatch command
    dispatch_parser = subparsers.add_parser(
        "dispatch", help="Determine agent role based on labels"
    )
    dispatch_parser.add_argument(
        "--labels",
        help="Comma-separated PR labels (required unless --get-trigger is used)",
    )
    dispatch_parser.add_argument("--config-path", help="Path to config file (optional)")
    dispatch_parser.add_argument(
        "--get-trigger",
        action="store_true",
        help="Return the trigger_label defined in the config instead of evaluating a role",
    )
    dispatch_parser.add_argument(
        "--get-context",
        action="store_true",
        help="Return the context file mapped to the matched role instead of the role name",
    )

    # process-diff command (virtual queue) - Deprecated
    diff_parser = subparsers.add_parser(
        "process-diff",
        help="[DEPRECATED] Run the issue creation automation from git diff",
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
        help="Directory to move task files to after issue creation (archive directory)",
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

    try:
        if args.command == "init":
            init_project(args)
        elif args.command == "process":
            run_process(args)
        elif args.command == "check":
            run_check(args)
        elif args.command == "relay":
            run_relay(args)
        elif args.command == "sync-relay":
            run_sync_relay(args)
        elif args.command == "visualize":
            run_visualize(args)
        elif args.command == "dispatch":
            run_dispatch(args)
        elif args.command == "process-diff":
            run_automation(args)
        else:
            parser.print_help()
            sys.exit(1)
    except SecurityValidationError as e:
        handler = ICKErrorHandler()
        err_data = ValidationErrorData(
            path="input",
            line=0,
            code="SECURITY_FAIL",
            message=str(e),
        )
        print(handler.format(err_data, no_color=args.no_color), file=sys.stderr)
        sys.exit(1)

    sys.exit(0)


if __name__ == "__main__":
    main()
