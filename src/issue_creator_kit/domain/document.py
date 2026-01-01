import re
from typing import Any

import yaml

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper  # type: ignore


class Document:
    def __init__(self, content: str, metadata: dict[str, Any]):
        self.content = content
        self.metadata = metadata

    @classmethod
    def parse(cls, text: str) -> "Document":
        """
        Parse text content into metadata and body.
        Supports YAML frontmatter and simple markdown list metadata.
        """
        metadata: dict[str, Any] = {}
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
                        metadata = parsed_yaml
                        # Convert first char of body if it starts with newline
                        if body.startswith("\n"):
                            body = body[1:]
                        content = body
                        return cls(content, metadata)
            except Exception:
                # Fallback to standard parsing if YAML fails
                pass

        # 2. Markdown List Metadata (- **Key**: Value)
        metadata = {}
        metadata_pattern = re.compile(r"^- \*\*([^*]+)\*\*: (.*)$")

        lines = text.splitlines()
        body_start_idx = 0
        metadata_found = False

        for i, line in enumerate(lines):
            match = metadata_pattern.match(line)
            if match:
                key, value = match.groups()
                metadata[key] = value.strip()
                metadata_found = True
                body_start_idx = i + 1
            elif metadata_found and not line.strip():
                body_start_idx = i + 1
            elif (
                metadata_found or i > 15
            ):  # Stop searching after 15 lines if no metadata found
                break

        if metadata:
            content = "\n".join(lines[body_start_idx:])

        return cls(content, metadata)

    def to_string(self, use_frontmatter: bool = True) -> str:
        """
        Serialize document back to string.
        """
        if use_frontmatter:
            yaml_content = yaml.dump(
                self.metadata,
                Dumper=Dumper,
                default_flow_style=False,
                allow_unicode=True,
            ).strip()
            return f"---\n{yaml_content}\n---\n{self.content}"
        # Markdown list format
        metadata_lines = [
            f"- **{key}**: {value}" for key, value in self.metadata.items()
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
            # Re-calculate header index in body_lines
            for line in body_lines:
                new_content.append(line)
                if not inserted and line.startswith("# "):
                    # Check if next line is empty
                    new_content.append("")
                    new_content.extend(metadata_lines)
                    new_content.append("")
                    inserted = True
            return "\n".join(new_content)
        return "\n".join(metadata_lines) + "\n\n" + "\n".join(body_lines)
