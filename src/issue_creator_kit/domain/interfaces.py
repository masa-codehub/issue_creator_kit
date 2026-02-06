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

    @abstractmethod
    def get_current_branch(self) -> str:
        pass

    @abstractmethod
    def checkout(
        self, branch: str, create: bool = False, base: str | None = None
    ) -> None:
        pass

    @abstractmethod
    def add(self, paths: list[str]) -> None:
        pass

    @abstractmethod
    def commit(self, message: str) -> None:
        pass

    @abstractmethod
    def push(
        self, remote: str = "origin", branch: str = "main", set_upstream: bool = False
    ) -> None:
        pass

    @abstractmethod
    def fetch(self, remote: str = "origin", prune: bool = False) -> None:
        pass


class IGitHubAdapter(ABC):
    @abstractmethod
    def create_issue(
        self, title: str, body: str, labels: list[str] | None = None
    ) -> int:
        pass

    @abstractmethod
    def create_pull_request(
        self, title: str, body: str, head: str, base: str
    ) -> tuple[str, int]:
        pass

    @abstractmethod
    def add_labels(self, issue_number: int, labels: list[str]) -> None:
        pass
