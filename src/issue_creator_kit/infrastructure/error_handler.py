import json
import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass
class ValidationErrorData:
    path: str | Path
    line: int
    code: str
    message: str
    field: str | None = None
    current_value: Any = None
    expected_value: Any = None

    def __str__(self) -> str:
        field_part = f" ({self.field})" if self.field else ""
        return f"{self.path}:{self.line}{field_part}: {self.message}"

    def __repr__(self) -> str:
        return f"ValidationErrorData(path={self.path!r}, line={self.line!r}, code={self.code!r}, message={self.message!r})"


class ICKErrorHandler:
    """Handles translation and formatting of validation errors.

    This class transforms structured validation errors (from Pydantic or Domain)
    into human-friendly messages in Japanese, following the project's UX spec.
    """

    # Translation map based on docs/specs/interface/error-reporting.md
    TRANSLATION_MAP = {
        "MISSING_FIELD": "{field} は必須項目です。YAML Frontmatter に追加してください",
        "INVALID_ID": "ID 形式が不正です。期待される形式: task-XXX-NN (例: task-014-01)",
        "JSON Syntax Error": "設定ファイルの構文が不正です。カンマやクォーテーションの不足がないか確認してください",
        "DUPLICATE_ID": "この ID は既に使用されています（アーカイブ済みまたは他のファイルと重複）。",
        "CYCLE_DETECTED": "循環依存が検出されました。依存関係を見直してください。",
        "SECURITY_FAIL": "{message}",
    }

    # Special handling for certain error messages if code doesn't match directly
    MESSAGE_REPLACEMENT = {
        "Invalid Task ID format": "ID 形式が不正です。期待される形式: task-XXX-NN (例: task-014-01)",
    }

    def format(self, error: ValidationErrorData, no_color: bool = False) -> str:
        """Format the error data into a human-friendly string.

        Args:
            error: The structured validation error data.
            no_color: If True, disable ANSI color codes regardless of environment.

        Returns:
            A formatted multi-line string ready for stderr.
        """

        # Determine if we should use color
        use_color = not no_color and "NO_COLOR" not in os.environ

        red = "\033[31m" if use_color else ""
        reset = "\033[0m" if use_color else ""

        # Translate message
        friendly_message = self._translate(error)

        # Build main line
        # Layout: [FAIL] <Path>:<Line> (<Field>): <Friendly Message>
        # Special case for Security errors: [SECURITY FAIL] <Message>
        if error.code == "SECURITY_FAIL":
            main_line = f"{red}[SECURITY FAIL]{reset} {friendly_message}"
        else:
            field_part = f" ({error.field})" if error.field else ""
            path_part = f" {error.path}:{error.line}{field_part}:"
            main_line = f"{red}[FAIL]{reset}{path_part} {friendly_message}"

        lines = [main_line]

        # Add Current/Expected lines if present
        if error.current_value is not None:
            lines.append(f"       Current: {error.current_value}")
        if error.expected_value is not None:
            lines.append(f"       Expected: {error.expected_value}")

        return "\n".join(lines)

    def _translate(self, error: ValidationErrorData) -> str:
        # 1. Try by code
        if error.code == "CYCLE_DETECTED":
            # Special handling for cycle to show path
            match = re.search(r"involves (\[.*\])", error.message)
            if match:
                try:
                    # Replace single quotes with double quotes for json.loads
                    cycle_ids = json.loads(match.group(1).replace("'", '"'))
                    cycle_str = " -> ".join(cycle_ids)
                    return f"循環依存が検出されました: {cycle_str}"
                except Exception:
                    pass
            return self.TRANSLATION_MAP["CYCLE_DETECTED"]

        if error.code in self.TRANSLATION_MAP:
            template = self.TRANSLATION_MAP[error.code]
            return template.format(field=error.field or "項目", message=error.message)

        # 2. Try by message (partial match)
        for key, replacement in self.MESSAGE_REPLACEMENT.items():
            if key in error.message:
                return replacement

        # 3. Try by regex or fuzzy match on message
        if "ID mismatch" in error.message:
            return f"ID が一致しません。{error.message}"

        # Fallback to original message
        return error.message
