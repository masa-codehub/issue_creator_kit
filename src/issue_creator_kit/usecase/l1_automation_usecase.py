import json
import logging
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

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

            # Search by label "adr:{number}" and "L1"
            labels = self.get_labels(adr.id)
            existing_issue = self.github.search_issues_by_label(labels)

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
    def get_labels(adr_id: str) -> list[str]:
        """
        Generate labels for the issue.
        Format: ['adr:{number}', 'L1']
        Example: 'adr-009' -> ['adr:009', 'L1']
        """
        # Extract number from 'adr-XXX' or 'adr-XXX-slug'
        match = re.search(r"adr-(\d{3})", adr_id)
        if match:
            number = match.group(1)
            return [f"adr:{number}", "L1"]
        # Fallback if ID doesn't match standard pattern (though Scanner validates it)
        return [f"adr:{adr_id}", "L1"]

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
