import logging
from pathlib import Path
from typing import Any, TypedDict

from issue_creator_kit.domain.interfaces import IGitHubAdapter
from issue_creator_kit.domain.models.document import ADR
from issue_creator_kit.domain.services.scanner import FileSystemScanner
from issue_creator_kit.usecase.l1_automation_usecase import L1AutomationUseCase
from issue_creator_kit.usecase.task_activation_usecase import (
    ActivationStatus,
    TaskActivationUseCase,
)

logger = logging.getLogger(__name__)


class Config(TypedDict, total=False):
    labels: list[str]
    exclude_patterns: list[str]


class OrchestrationResult(TypedDict):
    success: bool
    l1_issue: int | None
    l1_url: str | None
    l1_adr_id: str | None
    l2_issues: list[int]
    failed_tasks: list[str]
    new_l1: bool


class OrchestratorService:
    """
    Orchestrates the full flow of ADR-013:
    1. ADR (L1) Automation: Sync ADRs from _approved to GitHub.
    2. Task (L2) Activation: Chained activation of tasks for the active ADR context.

    Policies:
    - ADRs remain in _approved (handled by L1AutomationUseCase).
    - Tasks are moved to _archive upon successful issue creation (handled by TaskActivationUseCase).
    """

    def __init__(
        self,
        l1_usecase: L1AutomationUseCase,
        task_usecase: TaskActivationUseCase,
        scanner: FileSystemScanner,
        github: IGitHubAdapter,
    ):
        self.l1_usecase = l1_usecase
        self.task_usecase = task_usecase
        self.scanner = scanner
        self.github = github

    def execute(
        self,
        root_path: Path | str,
        dry_run: bool = False,
        config: Config | None = None,
    ) -> OrchestrationResult:
        """
        Execute the orchestration flow.
        """
        root_path = Path(root_path)
        config = config or {}

        # Scan once for both use cases
        exclude_patterns = config.get("exclude_patterns")
        documents, processed_ids = self.scanner.scan(
            root_path, exclude_patterns=exclude_patterns
        )

        # 1. ADR (L1) Automation
        issue_details = self.l1_usecase.execute(
            root_path, dry_run=dry_run, documents=documents
        )

        l1_id = None
        l1_url = None
        l1_adr_id = None

        if issue_details:
            detail = issue_details[0]
            l1_id = detail["number"]
            l1_url = detail["url"]
            l1_adr_id = detail["adr_id"]
            logger.info(f"[DONE] Created L1 Issue for {l1_adr_id}. ID: {l1_id}")
        else:
            # Search for existing L1 issue if no new ones created
            if dry_run:
                logger.info("[DRY-RUN] No new ADRs detected.")
            else:
                logger.info(
                    "[INFO] No new ADRs detected. Searching for existing L1 issue..."
                )
                l1_info = self._find_existing_l1_info(documents)
                if l1_info:
                    l1_id = l1_info["number"]
                    l1_adr_id = l1_info["adr_id"]
                    l1_url = self.github.get_issue_url(l1_id)

        if not l1_id:
            if dry_run:
                return {
                    "success": True,
                    "l1_issue": None,
                    "l1_url": None,
                    "l1_adr_id": None,
                    "l2_issues": [],
                    "failed_tasks": [],
                    "new_l1": False,
                }
            logger.info("[INFO] No active ADR context found. Skipping task activation.")
            return {
                "success": True,
                "l1_issue": None,
                "l1_url": None,
                "l1_adr_id": None,
                "l2_issues": [],
                "failed_tasks": [],
                "new_l1": False,
            }

        # 2. Task (L2) Activation
        if dry_run:
            logger.info(f"[DRY-RUN] Would activate tasks for L1 Issue #{l1_id}")
            return {
                "success": True,
                "l1_issue": l1_id,
                "l1_url": l1_url,
                "l1_adr_id": l1_adr_id,
                "l2_issues": [],
                "failed_tasks": [],
                "new_l1": bool(issue_details),
            }

        logger.info(f"[INFO] Activating tasks for L1 Issue #{l1_id}...")
        result = self.task_usecase.execute(
            root_path, l1_id, documents=documents, processed_ids=processed_ids
        )

        success = result.status in (
            ActivationStatus.SUCCESS,
            ActivationStatus.PARTIAL_SUCCESS,
        )

        return {
            "success": success,
            "l1_issue": l1_id,
            "l1_url": l1_url,
            "l1_adr_id": l1_adr_id,
            "l2_issues": result.successful_issues,
            "failed_tasks": result.failed_tasks,
            "new_l1": bool(issue_details),
        }

    def _find_existing_l1_info(self, documents: list[Any]) -> dict[str, Any] | None:
        """Find existing L1 issue information by searching GitHub using labels from scanned ADR."""
        adrs = [doc for doc in documents if isinstance(doc, ADR)]

        if not adrs:
            return None

        if len(adrs) > 1:
            logger.warning(
                f"Multiple ADRs found: {[a.id for a in adrs]}. "
                "Please ensure only one ADR is active per repository."
            )
            return None

        target_adr = adrs[0]
        labels = L1AutomationUseCase.get_labels(target_adr.id)
        issue_no = self.github.search_issues_by_label(labels)

        if issue_no:
            return {"number": issue_no, "adr_id": target_adr.id}
        return None
