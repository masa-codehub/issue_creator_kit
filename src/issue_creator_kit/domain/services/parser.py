from pathlib import Path

import frontmatter
from pydantic import ValidationError as PydanticValidationError

from issue_creator_kit.domain.exceptions import (
    ValidationError as DomainValidationError,
)
from issue_creator_kit.domain.models.document import (
    ADR,
    Document,
    Task,
)


class DocumentParser:
    """Parser for Markdown files with YAML frontmatter into Domain Models."""

    def parse(self, file_path: Path | str) -> Task | ADR:
        """
        Parse a Markdown file and return a Task or ADR model.

        Raises:
            DomainValidationError: If the frontmatter is invalid or does not match Task/ADR schema.
            FileNotFoundError: If the file does not exist.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {path}")

        # 1. Extract ID from Filename (Validation/Supplement)
        filename_id = self._extract_id_from_filename(path)

        # 2. Load Frontmatter
        try:
            post = frontmatter.load(path)
        except Exception as e:
            raise DomainValidationError(f"Invalid YAML in {path}: {e}") from e

        metadata = post.metadata or {}

        # 3. Handle ID Logic (Priority: Frontmatter > Filename)
        frontmatter_id = metadata.get("id")

        if frontmatter_id and filename_id and frontmatter_id != filename_id:
            raise DomainValidationError(
                f"ID mismatch in {path}: frontmatter='{frontmatter_id}', filename='{filename_id}'"
            )

        # Determine final ID
        final_id = frontmatter_id or filename_id
        if not final_id:
            raise DomainValidationError(
                f"Missing ID in {path} (both frontmatter and filename)"
            )

        # Supplement metadata with extracted ID if missing or empty
        if not metadata.get("id"):
            metadata["id"] = final_id

        # 4. Mandatory 'type' check (ADR-013)
        if "type" not in metadata:
            raise DomainValidationError(f"Missing mandatory 'type' field in {path}")

        # 5. Validate using the Document TypeAdapter
        try:
            doc = Document.validate_python(metadata)
            doc.path = path
            doc.content = post.content.strip() if post.content else ""
            return doc
        except PydanticValidationError as e:
            # Wrap Pydantic error in DomainValidationError
            raise DomainValidationError(f"Validation error in {path}: {e}") from e

    def _extract_id_from_filename(self, path: Path) -> str | None:
        """
        Extract potential ADR or Task ID from filename.

        Note: This method only performs a shallow check (prefix matching).
        Strict format validation is delegated to the Domain Model (Pydantic).
        """
        stem = path.stem

        # If the filename starts with a prefix indicating it's an ADR or Task,
        # return the stem. The Pydantic model validator will perform the
        # detailed format validation, centralizing the logic.
        if stem.startswith("adr-") or stem.startswith("task-"):
            return stem

        return None
