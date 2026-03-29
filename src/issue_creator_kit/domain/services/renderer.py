import json
import re
from functools import lru_cache

from issue_creator_kit.domain.exceptions import (
    DependencyResolutionError,
    MetadataSerializationError,
)
from issue_creator_kit.domain.models.document import ADR, DocumentType, Task
from issue_creator_kit.domain.models.renderer import RenderedIssue


class IssueRenderer:
    """Domain service to render Task or ADR models into GitHub Issue format."""

    def render(
        self,
        doc: DocumentType,
        id_map: dict[str, int],
        completed_issue_nos: set[int] | None = None,
    ) -> RenderedIssue:
        """
        Render a Task or ADR model into a RenderedIssue VO.

        Args:
            doc: The Task or ADR model to render.
            id_map: Mapping from TaskID/ADRID to GitHub Issue Number.
            completed_issue_nos: Set of Issue Numbers that are completed.

        Returns:
            RenderedIssue containing title, body, and labels.
        """
        title = f"{doc.id}: {doc.title}"

        # 1. Resolve IDs in body
        content = self._resolve_ids(doc.content, doc.depends_on, id_map)

        # Build body sections
        sections = [content.strip()]

        # 2. Append Dependencies section
        deps_block = self._generate_dependencies_block(
            doc.depends_on, id_map, completed_issue_nos
        )
        if deps_block:
            sections.append(deps_block.strip())

        # 3. Append Metadata
        sections.append(self._generate_metadata_block(doc).strip())

        body = "\n\n".join(sections)

        # 4. Synthesis Labels
        labels = self._synthesize_labels(doc)

        return RenderedIssue(title=title, body=body, labels=labels)

    def _resolve_ids(
        self, content: str, depends_on: list[str], id_map: dict[str, int]
    ) -> str:
        """
        Replace TaskIDs/ADRIDs with #IssueNo in content.
        Ensures substring safety and validates dependencies.
        """
        # Validate all depends_on IDs are in id_map
        for dep_id in depends_on:
            if dep_id not in id_map:
                raise DependencyResolutionError(
                    f"Dependency ID '{dep_id}' not found in id_map."
                )

        if not id_map:
            return content

        # Sort keys by length descending to prevent substring collision
        sorted_ids = tuple(sorted(id_map.keys(), key=len, reverse=True))

        # Use cached pattern
        pattern = self._get_compiled_pattern(sorted_ids)

        def replace_match(match: re.Match) -> str:
            task_id = match.group(1)
            issue_no = id_map.get(task_id)
            if issue_no is not None:
                return f"#{issue_no}"
            return task_id  # Should not happen given the pattern

        return pattern.sub(replace_match, content)

    @lru_cache(maxsize=128)  # noqa: B019
    def _get_compiled_pattern(self, sorted_ids: tuple[str, ...]) -> re.Pattern:
        """
        Compile regex pattern for a given set of IDs.
        Cached to avoid re-compilation.

        Uses negative lookbehind and lookahead to ensure safe replacement
        without breaking longer IDs or being part of other words.
        Boundary includes word characters [a-zA-Z0-9_] and hyphens [-].
        """
        # (?<![A-Za-z0-9_-])ID(?![A-Za-z0-9_-])
        # This is more robust than \b for TaskIDs containing hyphens.
        boundary = r"[A-Za-z0-9_-]"
        pattern_str = (
            rf"(?<!{boundary})("
            + "|".join(re.escape(i) for i in sorted_ids)
            + rf")(?!{boundary})"
        )
        return re.compile(pattern_str)

    def _generate_dependencies_block(
        self,
        depends_on: list[str],
        id_map: dict[str, int],
        completed_issue_nos: set[int] | None = None,
    ) -> str:
        """
        Generate ## Dependencies section with checklist.
        Returns empty string if no dependencies.
        """
        if not depends_on:
            return ""

        completed_issue_nos = completed_issue_nos or set()

        lines = ["## Dependencies"]
        for dep_id in depends_on:
            # Note: _resolve_ids already validates that dep_id exists in id_map
            issue_no = id_map[dep_id]
            checked = "x" if issue_no in completed_issue_nos else " "
            # Format: - [ ] #123 (task-id)
            lines.append(f"- [{checked}] #{issue_no} ({dep_id})")

        return "\n".join(lines)

    def _generate_metadata_block(self, doc: DocumentType) -> str:
        """Generate machine-readable metadata block in HTML comment."""
        if isinstance(doc, Task):
            include_fields = {
                "id",
                "type",
                "parent",
                "title",
                "status",
                "role",
                "phase",
                "depends_on",
                "labels",
                "issue_id",
            }
        elif isinstance(doc, ADR):
            include_fields = {
                "id",
                "type",
                "title",
                "status",
                "date",
                "depends_on",
            }
        else:
            raise TypeError(f"Unsupported document type: {type(doc)}")

        data = doc.model_dump(mode="json", include=include_fields)

        try:
            json_str = json.dumps(data, ensure_ascii=False)
        except (TypeError, ValueError) as e:
            raise MetadataSerializationError(
                f"Failed to serialize metadata: {e}"
            ) from e

        # Robustness check: Ensure JSON does not contain HTML comment delimiters
        if "-->" in json_str or "<!--" in json_str:
            raise MetadataSerializationError(
                "Metadata contains HTML comment delimiters '<!--' or '-->' which would break the block."
            )

        # ADR-011 convention: \n\n<!-- metadata:{json} -->
        # With mandatory space padding for robustness
        return f"<!-- metadata:{json_str} -->"

    def _synthesize_labels(self, doc: DocumentType) -> list[str]:
        """
        Synthesize GitHub labels based on metadata and manual labels.
        Excludes 'gemini' and applies categorical sorting.
        """
        excluded = {"gemini"}
        seen: set[str] = set()
        final_labels: list[str] = []

        def add_labels(candidates: list[str], sort: bool = False) -> None:
            iterable = sorted(candidates) if sort else candidates
            for label in iterable:
                if label not in seen and label not in excluded:
                    final_labels.append(label)
                    seen.add(label)

        # 1. System Labels (type first, then adr:NNN / design:NNN)
        system: list[str] = [doc.type]
        if doc.adr_number is not None:
            # source_id determines label prefix (adr: or design:)
            source_id = doc.parent if isinstance(doc, Task) else doc.id
            prefix = "design" if source_id.startswith("design-") else "adr"
            system.append(f"{prefix}:{doc.adr_number:03d}")
        add_labels(system, sort=False)

        # 2. Attribute Labels (role, phase) - sorted A-Z
        attributes = []
        role = getattr(doc, "role", None)
        if role:
            attributes.append(role)
        phase = getattr(doc, "phase", None)
        if phase:
            attributes.append(phase)
        add_labels(attributes, sort=True)

        # 3. Manual Labels - sorted A-Z
        manual_labels = getattr(doc, "labels", [])
        add_labels(manual_labels, sort=True)

        return final_labels
