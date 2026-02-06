import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

from issue_creator_kit.domain.exceptions import ValidationError

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper  # type: ignore


class Metadata(BaseModel):
    model_config = ConfigDict(extra="allow")

    id: str = Field(..., pattern=r"^[a-z0-9-]+$")
    status: str
    date: str | None = None

    # Task specific fields
    parent: str | None = None
    parent_issue: str | int | None = None
    type: str | None = None
    phase: str | None = None
    depends_on: list[str] = Field(default_factory=list)
    issue_id: int | None = None
    labels: list[str] = Field(default_factory=list)
    roadmap: str | None = None

    @model_validator(mode="before")
    @classmethod
    def normalize_keys(cls, data: Any) -> Any:
        if not isinstance(data, dict):
            return data

        mapping = {
            "id": ["id", "ID"],
            "title": ["title", "タイトル"],
            "status": ["status", "ステータス"],
            "date": ["date", "日付"],
            "parent": ["parent", "親"],
            "type": ["type", "型"],
            "phase": ["phase", "フェーズ", "工程"],
            "depends_on": ["depends_on", "依存", "Depends-On"],
            "issue_id": ["issue_id", "issue", "Issue"],
            "labels": ["labels", "ラベル"],
            "roadmap": ["roadmap"],
        }

        normalized = {}
        # Convert all keys to lowercase first for comparison
        lowered_data = {k.lower(): v for k, v in data.items()}

        # Mapping based on defined aliases
        for canonical, aliases in mapping.items():
            for alias in aliases:
                alias_lower = alias.lower()
                if alias_lower in lowered_data:
                    normalized[canonical] = lowered_data.pop(alias_lower)
                    break

        # Add remaining fields
        normalized.update(lowered_data)
        return normalized

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str, info: Any) -> str:
        # Determine valid statuses based on document type (simplified check)
        # ADR statuses: Draft, Approved, Postponed, Superseded
        # Task statuses: Draft, Ready, Issued, Completed, Cancelled
        valid_statuses = {
            "Draft",
            "Approved",
            "Postponed",
            "Superseded",
            "Ready",
            "Issued",
            "Completed",
            "Cancelled",
        }
        if v not in valid_statuses:
            raise ValueError(f"Invalid status: {v}")
        return v

    @model_validator(mode="after")
    def validate_logic(self) -> "Metadata":
        # Task specific validation
        if self.type in ("task", "integration"):
            if not self.parent:
                raise ValueError("Tasks must have a 'parent' field")
            if not self.phase:
                raise ValueError("Tasks must have a 'phase' field")

        # Issued/Completed must have issue_id
        if self.status in ("Issued", "Completed") and self.issue_id is None:
            raise ValueError(f"Status '{self.status}' requires an 'issue_id'")

        return self

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def keys(self) -> Iterable[str]:
        return self.model_dump().keys()

    def items(self) -> Iterable[tuple[str, Any]]:
        return self.model_dump().items()

    def update(self, updates: dict[str, Any]) -> None:
        # Re-validate after update by creating a new instance
        # model_copy does not validate and cannot add new extra fields
        data = self.model_dump()
        data.update(updates)
        new_obj = Metadata(**data)
        self.__dict__.update(new_obj.__dict__)
        # Ensure extra fields are copied for Pydantic v2
        if hasattr(new_obj, "__pydantic_extra__"):
            object.__setattr__(self, "__pydantic_extra__", new_obj.__pydantic_extra__)


class Document:
    def __init__(self, content: str, metadata: Metadata, path: Path | None = None):
        self.content = content
        self.metadata = metadata
        self.path = path

    @classmethod
    def parse(cls, text: str, path: Path | None = None) -> "Document":
        """
        Parse text content into metadata and body.
        Supports YAML frontmatter and simple markdown list metadata.
        """
        raw_metadata: dict[str, Any] = {}
        content = text

        # 1. YAML Frontmatter
        if text.startswith("---"):
            try:
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    yaml_text = parts[1]
                    body = parts[2]
                    parsed_yaml = yaml.safe_load(yaml_text)
                    if isinstance(parsed_yaml, dict):
                        raw_metadata = parsed_yaml
                        if body.startswith("\n"):
                            body = body[1:]
                        content = body
            except yaml.YAMLError:
                # Fallback to list parsing? Usually YAML errors should be reported
                pass
        else:
            # 2. Markdown List Metadata (- **Key**: Value)
            metadata_pattern = re.compile(r"^- \*\*([^*]+)\*\*: (.*)$")
            lines = text.splitlines()
            body_start_idx = 0
            metadata_found = False

            for i, line in enumerate(lines):
                match = metadata_pattern.match(line)
                if match:
                    key, value = match.groups()
                    raw_metadata[key] = value.strip()
                    metadata_found = True
                    body_start_idx = i + 1
                elif metadata_found and not line.strip():
                    body_start_idx = i + 1
                elif metadata_found or i > 15:
                    break
            if metadata_found:
                content = "\n".join(lines[body_start_idx:])

        try:
            metadata = Metadata(**raw_metadata)
        except Exception as e:
            raise ValidationError(str(e)) from e

        return cls(content, metadata, path)

    def to_string(self, use_frontmatter: bool = True) -> str:
        """
        Serialize document back to string.
        """
        if use_frontmatter:
            # Dump including extra fields
            yaml_content = yaml.dump(
                self.metadata.model_dump(),
                Dumper=Dumper,
                default_flow_style=False,
                allow_unicode=True,
                sort_keys=False,
            ).strip()
            return f"---\n{yaml_content}\n---\n{self.content}"

        # Markdown list format
        metadata_dict = self.metadata.model_dump()
        metadata_lines = [
            f"- **{key}**: {value}"
            for key, value in metadata_dict.items()
            if value is not None
        ]

        # Try to insert after title
        lines = self.content.splitlines()
        header_line_idx = -1
        for i, line in enumerate(lines):
            if line.startswith("# "):
                header_line_idx = i
                break

        body_lines = [
            line for line in lines if not re.match(r"^- \*\*([^*]+)\*\*: (.*)$", line)
        ]

        if header_line_idx != -1:
            new_content = []
            inserted = False
            for line in body_lines:
                new_content.append(line)
                if not inserted and line.startswith("# "):
                    new_content.append("")
                    new_content.extend(metadata_lines)
                    new_content.append("")
                    inserted = True
            return "\n".join(new_content)
        return "\n".join(metadata_lines) + "\n\n" + "\n".join(body_lines)
