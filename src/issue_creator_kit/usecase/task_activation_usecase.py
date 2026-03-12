import logging
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

from issue_creator_kit.domain.exceptions import (
    DomainError,
    GitHubAPIError,
)
from issue_creator_kit.domain.interfaces import IFileSystemAdapter, IGitHubAdapter
from issue_creator_kit.domain.models.document import Task
from issue_creator_kit.domain.services.builder import GraphBuilder
from issue_creator_kit.domain.services.l1_sync import L1SyncService
from issue_creator_kit.domain.services.renderer import IssueRenderer
from issue_creator_kit.domain.services.scanner import FileSystemScanner

logger = logging.getLogger(__name__)


class ActivationStatus(Enum):
    SUCCESS = "SUCCESS"
    PARTIAL_SUCCESS = "PARTIAL_SUCCESS"
    FAILED = "FAILED"


@dataclass
class ActivationResult:
    successful_issues: list[int]
    failed_tasks: list[str]
    status: ActivationStatus


class TaskActivationUseCase:
    """
    Orchestrates the activation of tasks: scan, sort, propagate IDs, create issues, sync L1, and archive.
    """

    def __init__(
        self,
        scanner: FileSystemScanner,
        builder: GraphBuilder,
        github: IGitHubAdapter,
        fs: IFileSystemAdapter,
        l1_sync: L1SyncService,
        renderer: IssueRenderer,
    ):
        self.scanner = scanner
        self.builder = builder
        self.github = github
        self.fs = fs
        self.l1_sync = l1_sync
        self.renderer = renderer

    def execute(
        self,
        root_path: Path | str,
        l1_id: int,
        documents: list[Any] | None = None,
        processed_ids: dict[str, int] | None = None,
    ) -> ActivationResult:
        root_path = Path(root_path)

        # Step 1: Scanning
        all_docs: list[Any]
        all_processed_ids: dict[str, int]

        if documents is not None and processed_ids is not None:
            all_docs = documents
            all_processed_ids = processed_ids
        else:
            try:
                all_docs, all_processed_ids = self.scanner.scan(root_path)
            except DomainError as e:
                logger.error(f"Scan failed (DomainError): {e}")
                return ActivationResult([], [], ActivationStatus.FAILED)
            except Exception as e:
                logger.error(f"Scan failed (Unexpected): {e}")
                return ActivationResult([], [], ActivationStatus.FAILED)

        # Filter only Tasks
        tasks = [doc for doc in all_docs if isinstance(doc, Task)]
        if not tasks:
            return ActivationResult([], [], ActivationStatus.SUCCESS)

        # Step 2: Sorting
        try:
            # Pass ALL documents to build_graph so ADR dependencies are resolved
            graph = self.builder.build_graph(all_docs, all_processed_ids)
            execution_order = graph.get_execution_order()
        except DomainError as e:
            logger.error(f"Sort failed (DomainError): {e}")
            return ActivationResult([], [], ActivationStatus.FAILED)
        except Exception as e:
            logger.error(f"Sort failed (Unexpected): {e}")
            return ActivationResult([], [], ActivationStatus.FAILED)

        task_map = {task.id: task for task in tasks}

        # Initialize map with archived task IDs and their issue numbers.
        # Filter processed_ids to keep only those that have a non-zero issue_no.
        in_memory_map: dict[str, int] = {
            k: v for k, v in all_processed_ids.items() if v > 0
        }
        successful_issues: list[int] = []
        failed_tasks: list[str] = []

        # Step 3: Sequential Creation & Virtual Propagation
        for task_id in execution_order:
            if task_id not in task_map:
                continue

            task = task_map[task_id]

            try:
                if not task.path:
                    raise DomainError(f"Task {task_id} has no path")

                # 3.1 Idempotency check
                issue_no = self._check_idempotency(task, root_path)
                if issue_no:
                    logger.info(
                        f"Task {task_id} already has issue #{issue_no}. Skipping creation."
                    )
                    in_memory_map[task_id] = issue_no
                    successful_issues.append(issue_no)
                    # Even if already exists, ensure it is archived (Step 5)
                    self._archive_task(task, issue_no, root_path)
                    continue

                # 3.2 Render Issue (ID resolution & Metadata injection)
                rendered = self.renderer.render(task, in_memory_map.copy())

                # 3.3 Create Issue
                issue_no = self.github.create_issue(
                    title=rendered.title, body=rendered.body, labels=rendered.labels
                )

                in_memory_map[task_id] = issue_no
                successful_issues.append(issue_no)

                # Step 5: Physical Fixation (Archive)
                self._archive_task(task, issue_no, root_path)

            except DomainError as e:
                logger.error(f"DomainError processing task {task_id}: {e}")
                failed_tasks.append(task_id)
                continue
            except (GitHubAPIError, ValueError, OSError) as e:
                logger.error(f"Unexpected error processing task {task_id}: {e}")
                failed_tasks.append(task_id)
                # Recoverable error policy: continue with remaining tasks but status becomes PARTIAL_SUCCESS
                continue

        # Step 4: L1 Checklist Sync
        if in_memory_map:
            try:
                self.l1_sync.sync_checklist(l1_id, in_memory_map)
            except Exception as e:
                logger.warning(f"L1 Sync failed: {e}")

        # Step 6: Initial Ignition (ADR-015)
        self._ignite_independent_tasks(tasks, in_memory_map)

        status = ActivationStatus.SUCCESS
        if failed_tasks:
            status = (
                ActivationStatus.PARTIAL_SUCCESS
                if successful_issues
                else ActivationStatus.FAILED
            )

        return ActivationResult(successful_issues, failed_tasks, status)

    def _ignite_independent_tasks(
        self, tasks: list[Task], in_memory_map: dict[str, int]
    ) -> None:
        """
        Add 'gemini' label to independent tasks (best-effort).
        """
        # Filter independent tasks that have been successfully mapped to an issue number
        ignitable_tasks = [
            (task, in_memory_map[task.id])
            for task in tasks
            if not task.depends_on and in_memory_map.get(task.id) is not None
        ]

        if not ignitable_tasks:
            return

        logger.info(f"Starting initial ignition for {len(ignitable_tasks)} tasks")

        for task, issue_no in ignitable_tasks:
            try:
                self.github.add_labels(issue_no, ["gemini"])
                logger.info(f"Ignited task {task.id} (Issue #{issue_no})")
            except GitHubAPIError as e:
                # Best-effort: log and continue
                logger.warning(
                    f"Failed to ignite task {task.id} (Issue #{issue_no}): {e}"
                )

    def _check_idempotency(self, task: Task, root_path: Path) -> int | None:
        # Check archive first
        archive_dir = root_path / "tasks" / "_archive"
        if archive_dir.exists():
            pattern = f"{task.id}-*.md"
            matches = list(archive_dir.glob(pattern))
            if matches:
                # If multiple matches found, warn and use the last one (likely most recent)
                if len(matches) > 1:
                    matches.sort()  # Sort to ensure deterministic selection
                    logger.warning(
                        f"Multiple archive files found for {task.id}: {matches}. Using {matches[-1]}"
                    )

                # task-010-01-123.md
                filename = matches[-1].stem
                issue_no_str = filename.split("-")[-1]
                if issue_no_str.isdigit():
                    return int(issue_no_str)

        # Check GitHub (Search by exact Title)
        title = f"{task.id}: {task.title}"
        return self.github.find_issue_by_title(title)

    def _archive_task(self, task: Task, issue_no: int, root_path: Path) -> None:
        if not task.path:
            raise DomainError(f"Task {task.id} has no path")

        dst_path = root_path / "tasks" / "_archive" / f"{task.id}-{issue_no}.md"

        try:
            # Use overwrite=True to ensure the source file is moved even if the destination exists.
            # This prevents files from remaining in reqs/tasks/ during retries or syncs.
            self.fs.move_file(task.path, dst_path, overwrite=True)
            logger.info(f"Task {task.id} archived to {dst_path}")
        except FileNotFoundError:
            # Source file might have been moved already by another process or manual action
            logger.info(
                f"Task {task.id} source file not found, likely already archived."
            )
        except Exception as e:
            logger.error(f"Archive failed for {task.id}: {e}")
            raise
