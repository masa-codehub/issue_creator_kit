from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from issue_creator_kit.domain.document import Document


class IFileSystemAdapter(ABC):
    @abstractmethod
    def read_document(self, file_path: Path) -> Document:
        pass

    @abstractmethod
    def save_document(
        self, file_path: Path, document: Document, use_frontmatter: bool = True
    ) -> None:
        pass

    @abstractmethod
    def update_metadata(self, file_path: Path, updates: dict[str, Any]) -> None:
        pass

    @abstractmethod
    def list_files(self, dir_path: Path, pattern: str = "*") -> list[Path]:
        pass


class IGitAdapter(ABC):
    @abstractmethod
    def get_added_files(self, base_ref: str, head_ref: str, path: str) -> list[str]:
        pass

    @abstractmethod
    def move_file(self, src: str, dst: str) -> None:
        pass


class IGitHubAdapter(ABC):
    @abstractmethod
    def create_issue(
        self, title: str, body: str, labels: list[str] | None = None
    ) -> int:
        pass
