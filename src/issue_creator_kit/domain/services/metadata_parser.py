import json

from pydantic import ValidationError as PydanticValidationError

from issue_creator_kit.domain.constants import RE_METADATA
from issue_creator_kit.domain.exceptions import (
    MetadataNotFoundError,
    MetadataParseError,
    MetadataValidationError,
)
from issue_creator_kit.domain.models.document import ADR, Document, Task


class MetadataParser:
    """Extracts and validates Task/ADR metadata from the issue body."""

    def parse(self, body: str) -> Task | ADR:
        """
        Extracts and validates Task/ADR metadata from the issue body.
        Also preserves the original content before metadata/dependencies.
        Raises: MetadataNotFoundError, MetadataParseError, MetadataValidationError
        """
        # 1. Extract content (everything before ## Dependencies or <!-- metadata:)
        content_end = len(body)
        meta_match = RE_METADATA.search(body)
        if meta_match:
            content_end = min(content_end, meta_match.start())

        deps_header = "## Dependencies"
        deps_idx = body.find(deps_header)
        if deps_idx != -1:
            content_end = min(content_end, deps_idx)

        content = body[:content_end].strip()

        # 2. Extract and validate metadata
        matches = RE_METADATA.findall(body)
        if not matches:
            raise MetadataNotFoundError("No metadata tag found in the issue body.")

        # Select the last match (priority)
        last_metadata_str = matches[-1].strip()

        # Decode JSON
        try:
            # 仕様に従い、json.JSONDecoder().raw_decode を使用してメタデータをデコードする。
            decoder = json.JSONDecoder()
            data, idx = decoder.raw_decode(last_metadata_str)

            # Ensure there are no non-whitespace trailing characters after the JSON
            if last_metadata_str[idx:].strip():
                raise MetadataParseError(
                    "Failed to parse metadata JSON: unexpected trailing characters."
                )
        except json.JSONDecodeError as e:
            raise MetadataParseError(f"Failed to parse metadata JSON: {e}") from e

        # Validate using Document TypeAdapter (supports Task and ADR via discrimination)
        try:
            doc = Document.validate_python(data)
            doc.content = content
            return doc
        except PydanticValidationError as e:
            raise MetadataValidationError(f"Metadata validation failed: {e}") from e
