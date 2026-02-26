import json
import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from issue_creator_kit.domain.exceptions import (
    GraphError,
)
from issue_creator_kit.domain.exceptions import (
    ValidationError as DomainValidationError,
)
from issue_creator_kit.domain.services.builder import GraphBuilder
from issue_creator_kit.domain.services.parser import DocumentParser
from issue_creator_kit.domain.services.scanner import FileSystemScanner
from issue_creator_kit.infrastructure.error_handler import ValidationErrorData

logger = logging.getLogger(__name__)


@dataclass
class ValidationResult:
    valid: bool
    errors: list[ValidationErrorData] = field(default_factory=list)


class TaskGraphValidator:
    def __init__(
        self,
        parser: DocumentParser | None = None,
        builder: GraphBuilder | None = None,
        scanner: FileSystemScanner | None = None,
    ):
        self.parser = parser or DocumentParser()
        self.builder = builder or GraphBuilder()
        self.scanner = scanner or FileSystemScanner(self.parser)

    def validate(self, root_path: Path | str) -> ValidationResult:
        root = Path(root_path)
        errors = []

        # 1. Get archived IDs (needed for GraphBuilder and duplicate check)
        archived_ids: dict[str, int] = {}
        try:
            # We use scanner to get archived IDs.
            # exclude_patterns=["*"] effectively skips scanning new files but still processes archive.
            _, archived_ids = self.scanner.scan(root, exclude_patterns=["*"])
        except Exception as e:
            # If scanner fails on archive, we record it and continue
            errors.append(
                ValidationErrorData(
                    path="_archive",
                    line=1,
                    code="SCAN_ERROR",
                    message=f"Failed to scan archive: {e}",
                )
            )

        # 2. Collect all potential files to scan (Collect multiple parse/duplicate errors)
        # Note: We don't use self.scanner.scan() directly because it fails fast on first error.

        # Re-implementing parts of scanner logic to collect all errors
        scan_targets = [root / "design" / "_approved"]
        tasks_dir = root / "tasks"
        if tasks_dir.exists():
            for child in tasks_dir.iterdir():
                if child.is_dir() and child.name != "_archive":
                    scan_targets.append(child)

        documents = []
        seen_ids: dict[str, Path] = {}  # id -> path

        for target in scan_targets:
            if not target.exists():
                continue
            for file_path in target.rglob("*.md"):
                if "_archive" in file_path.parts:
                    continue

                try:
                    doc = self.parser.parse(file_path)
                    if doc.id in archived_ids:
                        line = self._find_line_number(file_path, f"id: {doc.id}")
                        errors.append(
                            ValidationErrorData(
                                path=file_path.relative_to(root),
                                line=line,
                                field="id",
                                code="DUPLICATE_ID",
                                message=f"DUPLICATE_ID '{doc.id}' (Already archived)",
                                current_value=doc.id,
                            )
                        )
                    elif doc.id in seen_ids:
                        prev_path = seen_ids[doc.id]
                        line = self._find_line_number(file_path, f"id: {doc.id}")
                        errors.append(
                            ValidationErrorData(
                                path=file_path.relative_to(root),
                                line=line,
                                field="id",
                                code="DUPLICATE_ID",
                                message=f"DUPLICATE_ID '{doc.id}' already exists in {prev_path.relative_to(root)}",
                                current_value=doc.id,
                            )
                        )
                    else:
                        documents.append(doc)
                        seen_ids[doc.id] = file_path
                except DomainValidationError as e:
                    line = 1
                    msg = str(e)
                    field_name = e.field
                    code = "VALIDATION_ERROR"
                    current_val = None
                    expected_val: str | None = None

                    # Try to extract more info from the error
                    if "ID mismatch" in msg:
                        line = self._find_line_number(file_path, "id:")
                        field_name = "id"
                        code = "ID_MISMATCH"
                    elif "Validation error" in msg:
                        # Extract field name and details from Pydantic message if possible
                        # Pydantic v2 format:
                        # field_name
                        #   Error message [type=error_type, ...]

                        # Try to find the field name which is usually on its own line before the error type
                        field_match = re.search(
                            r"\n([\w.]+)\n\s+.*\[type=([\w.]+),", msg
                        )
                        if field_match:
                            field_name = field_match.group(1).split(".")[
                                -1
                            ]  # Use last part if dotted (e.g. adr.title -> title)
                            code = field_match.group(2)
                            line = self._find_line_number(file_path, f"{field_name}:")
                        else:
                            # Fallback to old regex just in case
                            match = re.search(r"([\w.]+)\s+\[type=([\w.]+),", msg)
                            if match:
                                field_name = match.group(1).split(".")[-1]
                                code = match.group(2)
                                line = self._find_line_number(
                                    file_path, f"{field_name}:"
                                )

                        # Normalize code
                        if code in ("missing", "value_error.missing"):
                            code = "MISSING_FIELD"
                        elif "Invalid Task ID format" in msg:
                            code = "INVALID_ID"
                            field_name = field_name or "id"
                            expected_val = "task-XXX-NN (例: task-014-01)"
                            # Update local vars for consistency
                            if current_val is None:
                                v_match = re.search(r"input_value='([^']+)'", msg)
                                if v_match:
                                    current_val = v_match.group(1)

                        # Extract current value if mentioned
                        val_match = re.search(r"input_value='([^']+)'", msg)
                        if val_match:
                            current_val = val_match.group(1)

                        # Re-calculate expected value for INVALID_ID if we already found it
                        if code == "INVALID_ID":
                            expected_val = "task-XXX-NN (例: task-014-01)"

                    errors.append(
                        ValidationErrorData(
                            path=file_path.relative_to(root),
                            line=line,
                            field=field_name,
                            code=code,
                            message=msg,
                            current_value=current_val,
                            expected_value=expected_val,
                        )
                    )
                except Exception as e:
                    errors.append(
                        ValidationErrorData(
                            path=file_path.relative_to(root),
                            line=1,
                            code="UNEXPECTED_ERROR",
                            message=str(e),
                        )
                    )

        # 3. Build and validate graph
        if documents:
            try:
                # Note: build_graph is fail-fast and will only report the first error.
                self.builder.build_graph(documents, archived_ids)
            except GraphError as e:
                # Find which document caused the error
                msg = str(e)
                involved_ids = re.findall(r"'([^']+)'", msg)

                # If it's a cycle, it might have a list-like representation
                if "CYCLE_DETECTED" in msg:
                    path_match = re.search(r"involves (\[.*\])", msg)
                    if path_match:
                        # Safer parsing than eval()
                        json_str = path_match.group(1).replace("'", '"')
                        try:
                            involved_ids = json.loads(json_str)
                        except Exception:
                            logger.warning(
                                f"Failed to parse cycle path JSON: {json_str}"
                            )

                if involved_ids:
                    # Find which involved ID corresponds to a document we scanned
                    target_id = None
                    for node_id in involved_ids:
                        if node_id in seen_ids:
                            target_id = node_id
                            # For Orphan, prefer the referrer (usually the last 'id' in the message)
                            if (
                                "referenced by" in msg
                                and node_id in msg.split("referenced by")[-1]
                            ):
                                target_id = node_id
                                break

                    if target_id:
                        file_path = seen_ids[target_id]
                        keyword = "id:"
                        if e.code == "SELF_REFERENCE" or e.code == "ORPHAN_DEPENDENCY":
                            # Use file content to determine which keyword to look for
                            try:
                                content = file_path.read_text(encoding="utf-8")
                                has_depends_on = "depends_on:" in content
                                has_parent = "parent:" in content

                                if has_depends_on:
                                    keyword = "depends_on:"
                                elif has_parent:
                                    keyword = "parent:"
                            except Exception:
                                logger.error(
                                    f"Failed to read file for keyword search: {file_path}"
                                )

                        line = self._find_line_number(file_path, keyword)
                        errors.append(
                            ValidationErrorData(
                                path=file_path.relative_to(root),
                                line=line,
                                code=e.code or "GRAPH_ERROR",
                                message=msg,
                            )
                        )
                    else:
                        errors.append(
                            ValidationErrorData(
                                path="unknown",
                                line=1,
                                code=e.code or "GRAPH_ERROR",
                                message=msg,
                            )
                        )
                else:
                    errors.append(
                        ValidationErrorData(
                            path="unknown",
                            line=1,
                            code=e.code or "GRAPH_ERROR",
                            message=msg,
                        )
                    )

        return ValidationResult(valid=len(errors) == 0, errors=errors)

    def _find_line_number(self, path: Path, keyword: str) -> int:
        try:
            content = path.read_text(encoding="utf-8")
            lines = content.splitlines()
            for i, line in enumerate(lines, 1):
                if keyword in line:
                    return i
        except Exception as e:
            logger.error(f"Failed to read file {path}: {e}")
        return 1
