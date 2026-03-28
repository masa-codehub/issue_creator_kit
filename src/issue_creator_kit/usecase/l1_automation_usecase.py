import json
import logging
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from issue_creator_kit.domain.constants import PHASE_ORDER
from issue_creator_kit.domain.exceptions import DomainError
from issue_creator_kit.domain.interfaces import IGitHubAdapter
from issue_creator_kit.domain.models.document import ADR
from issue_creator_kit.domain.services.scanner import FileSystemScanner

logger = logging.getLogger(__name__)


class L1AutomationUseCase:
    """
    UseCase for automating L1 Issue creation for ADRs.
    Follows ADR-009 requirements for search-based idempotency.
    """

    def __init__(
        self,
        scanner: FileSystemScanner,
        github: IGitHubAdapter,
    ):
        self.scanner = scanner
        self.github = github

    def execute(
        self,
        root_path: Path | str,
        dry_run: bool = False,
        documents: list[Any] | None = None,
    ) -> list[dict[str, Any]]:
        """
        Scan for ADRs in _approved and sync them to GitHub issues.

        Args:
            root_path: Path to the reqs directory.
            dry_run: If True, skip actual issue creation.
            documents: Optional pre-scanned documents. If None, scanner.scan() will be called.

        Returns:
            List of dictionaries containing issue details for newly created issues.
            Details: {'adr_id': str, 'number': int, 'url': str}
            Existing matched issues are not included.
        """
        all_docs: list[Any]
        if documents is not None:
            all_docs = documents
        else:
            all_docs, _ = self.scanner.scan(root_path)

        # 2. Filter for ADRs (ignore Tasks)
        adrs = [doc for doc in all_docs if isinstance(doc, ADR)]

        # 3. For each ADR, search GitHub issues (via `self.github`)
        unprocessed_adrs: list[ADR] = []

        for adr in adrs:
            # Check fail-fast condition before expensive API call
            if len(unprocessed_adrs) >= 2:
                # We already have at least 2, so the policy is violated.
                # No need to search further.
                break

            # Search by identity labels ("L1" and "{prefix}:{number}")
            # We separate identity from initial labels (arch/plan) to ensure
            # idempotency even if existing issues lack those labels.
            identity_labels = self.get_identity_labels(adr.id)
            existing_issue = self.github.search_issues_by_label(identity_labels)

            if existing_issue is None:
                unprocessed_adrs.append(adr)

        # 4. Strict One-ADR Policy
        count = len(unprocessed_adrs)

        if count == 0:
            return []

        if count >= 2:
            raise DomainError(
                f"Multiple unprocessed ADRs detected: {[a.id for a in unprocessed_adrs]} (and potentially more). "
                "Strict One-ADR Policy violation."
            )

        # Single unprocessed ADR found
        target_adr = unprocessed_adrs[0]

        if dry_run:
            logger.info(
                f"[DRY-RUN] Would create issue for {target_adr.id}: {target_adr.title}"
            )
            return []

        # Create Issue
        metadata = self._create_metadata(target_adr)
        body = self._prepare_issue_body(target_adr, metadata)
        labels = self.get_labels(target_adr.id)

        # Ensure labels exist before creating the issue
        self.github.ensure_labels_exist(labels)

        issue_number = self.github.create_issue(
            title=f"ADR: {target_adr.title}",
            body=body,
            labels=labels,
            metadata=None,
        )

        return [
            {
                "adr_id": target_adr.id,
                "number": issue_number,
                "url": self.github.get_issue_url(issue_number),
            }
        ]

    @staticmethod
    def sort_labels(labels: list[str]) -> list[str]:
        """
        Sort labels according to L1 Initial Labeling Strategy Specification.
        Order: [Phase, plan, L1, ID, Others...]
        """
        phase_labels = set(PHASE_ORDER)
        identity_pattern = re.compile(r"^(adr|design):\d{3}$")

        # Deduplicate
        unique_labels = list(set(labels))

        # 1. Identify categories
        found_phases = [label for label in unique_labels if label in phase_labels]
        found_plan = [label for label in unique_labels if label == "plan"]
        found_l1 = [label for label in unique_labels if label == "L1"]
        found_ids = [label for label in unique_labels if identity_pattern.match(label)]

        # 2. Others (sorted alphabetically)
        categorized = set(found_phases + found_plan + found_l1 + found_ids)
        others = sorted([label for label in unique_labels if label not in categorized])

        # 3. Construct final list
        # Standard: Exactly one phase, but if multiple exist (error state), we sort them.
        return sorted(found_phases) + found_plan + found_l1 + sorted(found_ids) + others

    @staticmethod
    def get_identity_labels(adr_id: str) -> list[str]:
        """
        Generate identity labels for searching existing issues.
        Format: ['L1', 'adr:NNN' or 'design:NNN']
        """
        match = re.search(r"^(adr|design)-(\d{3})", adr_id)
        if match:
            prefix = match.group(1)
            number = match.group(2)
            return L1AutomationUseCase.sort_labels([f"{prefix}:{number}", "L1"])

        # Error if ID doesn't match standard pattern
        raise DomainError(
            f"Invalid ADR/DesignDoc ID format: {adr_id}. "
            "Must be 'adr-XXX' or 'design-XXX'."
        )

    @staticmethod
    def get_labels(adr_id: str) -> list[str]:
        """
        Generate labels to be applied when creating a new issue.
        Includes phase ('arch' or 'spec'), 'plan', 'L1', and identity label.
        Order: [Phase, plan, L1, ID]
        """
        match = re.search(r"^(adr|design)-(\d{3})", adr_id)
        if match:
            prefix = match.group(1)
            number = match.group(2)
            phase = "spec" if prefix == "design" else "arch"
            return L1AutomationUseCase.sort_labels(
                [phase, "plan", "L1", f"{prefix}:{number}"]
            )

        # Error if ID doesn't match standard pattern
        raise DomainError(
            f"Invalid ADR/DesignDoc ID format: {adr_id}. "
            "Must be 'adr-XXX' or 'design-XXX'."
        )

    @staticmethod
    def _create_metadata(adr: ADR) -> dict[str, Any]:
        """Create metadata dictionary for ADR."""
        return {
            "adr_id": adr.id,
            "version": "1.0",
            "injected_at": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
        }

    @staticmethod
    def _prepare_issue_body(adr: ADR, metadata: dict[str, Any]) -> str:
        """
        Inject metadata as hidden comments into the issue body.
        """
        # Construct body content: prefer full content from doc, fallback to summary
        if adr.content:
            body = adr.content
        else:
            body = (
                f"# {adr.title}\n\n"
                f"**Status**: {adr.status}\n"
                f"**Date**: {adr.date}\n\n"
                f"See details in `{adr.id}`."
            )

        # Compact JSON serialization
        json_str = json.dumps(metadata, separators=(",", ":"))

        # HTML Comment format
        injection = f"<!-- metadata:{json_str} -->"

        return f"{body}\n\n{injection}"
