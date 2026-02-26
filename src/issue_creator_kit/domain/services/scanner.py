from pathlib import Path

import frontmatter

from issue_creator_kit.domain.exceptions import (
    ValidationError as DomainValidationError,
)
from issue_creator_kit.domain.models.document import ADR, Document, Task
from issue_creator_kit.domain.services.parser import DocumentParser


class FileSystemScanner:
    """Scanner for physical file system to detect unprocessed ADRs and Tasks."""

    def __init__(self, parser: DocumentParser):
        self.parser = parser

    def scan(
        self, root_path: Path | str, exclude_patterns: list[str] | None = None
    ) -> tuple[list[Task | ADR], dict[str, int]]:
        """
        Scan the file system for unprocessed documents and collect archived IDs and their issue numbers.

        Args:
            root_path: Base directory to scan (e.g., 'reqs/').
            exclude_patterns: Glob patterns to exclude from scanning.

        Returns:
            A tuple of (unprocessed_documents, processed_ids_mapping).
            processed_ids_mapping: dict mapping document ID to issue number (int).

        Raises:
            DomainValidationError: If duplicate IDs are found or metadata is invalid.
            FileNotFoundError: If root_path does not exist.
        """
        root = Path(root_path)
        if not root.exists():
            raise FileNotFoundError(f"Root path not found: {root}")

        exclude_patterns = exclude_patterns or []

        # 1. Collect Processed IDs from all _archive directories
        processed_ids: dict[str, int] = {}
        for archive_dir in root.rglob("_archive"):
            if not archive_dir.is_dir():
                continue

            for file_path in archive_dir.glob("*.md"):
                try:
                    # task-010-01-123.md -> 123
                    filename = file_path.stem
                    parts = filename.split("-")
                    issue_no = 0
                    if parts and parts[-1].isdigit():
                        issue_no = int(parts[-1])

                    post = frontmatter.load(file_path)
                    if not post.metadata:
                        continue

                    # Inject issue_id if found in filename and missing in metadata
                    if issue_no > 0 and "issue_id" not in post.metadata:
                        post.metadata["issue_id"] = issue_no

                    # Validate ID format using domain models
                    doc = Document.validate_python(post.metadata)
                    doc_id = doc.id

                    if doc_id in processed_ids:
                        raise DomainValidationError(
                            f"DUPLICATE_ID '{doc_id}' found in archive"
                        )
                    processed_ids[doc_id] = issue_no
                except Exception as e:
                    if isinstance(e, DomainValidationError):
                        raise e
                    # _archive 側のYAML破損や読み込み失敗も Fail-fast で報告する
                    raise DomainValidationError(
                        f"FAILED_TO_LOAD_ARCHIVED_DOCUMENT at '{file_path}': {type(e).__name__}: {e}"
                    ) from e

        # 2. Scan Unprocessed Files
        documents: list[Task | ADR] = []
        seen_in_scan: set[str] = set()

        # Directories to scan for unprocessed files
        scan_targets = [root / "design" / "_approved"]

        # Scan tasks subdirectories (tasks/*/) excluding _archive
        tasks_dir = root / "tasks"
        if tasks_dir.exists():
            for child in tasks_dir.iterdir():
                if child.is_dir() and child.name != "_archive":
                    scan_targets.append(child)

        for target in scan_targets:
            if not target.exists():
                continue

            # Recursive scan for Markdown files
            for file_path in target.rglob("*.md"):
                # Skip files in _archive directories
                if "_archive" in file_path.parts:
                    continue

                # Check exclude patterns
                if any(file_path.match(pattern) for pattern in exclude_patterns):
                    continue

                # Parse and validate
                try:
                    doc = self.parser.parse(file_path)
                    if doc.id in processed_ids:
                        raise DomainValidationError(
                            f"DUPLICATE_ID '{doc.id}' (Already archived)"
                        )
                    if doc.id in seen_in_scan:
                        raise DomainValidationError(
                            f"DUPLICATE_ID '{doc.id}' (Duplicate in scan)"
                        )

                    documents.append(doc)
                    seen_in_scan.add(doc.id)
                except Exception as e:
                    if isinstance(e, DomainValidationError):
                        raise e
                    # Unexpected errors should be reported
                    raise e

        return documents, processed_ids
