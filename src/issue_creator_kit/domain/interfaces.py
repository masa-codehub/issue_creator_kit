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

    @abstractmethod
    def move_file(self, src: Path, dst: Path, overwrite: bool = False) -> None:
        """Move a file to a new location."""
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
        self,
        title: str,
        body: str,
        labels: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> int:
        pass

    @abstractmethod
    def create_pull_request(
        self, title: str, body: str, head: str, base: str
    ) -> tuple[str, int]:
        pass

    @abstractmethod
    def get_issue(self, issue_number: int) -> dict[str, str]:
        """Get details (body and etag) of a specific issue."""
        pass

    @abstractmethod
    def find_issue_by_title(self, title: str) -> int | None:
        """
        Find an open issue with the exact same title.
        Returns: Issue number if found, otherwise None.
        """
        pass

    @abstractmethod
    def patch_issue(
        self, issue_number: int, body: str, etag: str | None = None
    ) -> None:
        """Update an issue body, optionally using an ETag for concurrency control."""
        pass

    @abstractmethod
    def add_labels(self, issue_number: int, labels: list[str]) -> None:
        pass

    @abstractmethod
    def update_issue_labels(self, issue_number: int, labels: list[str]) -> None:
        """
        Replace all existing labels of an issue with the given list.

        This method performs a full replacement of the issue's labels:
        all existing labels are removed first, and then the given labels
        are applied.

        IMPORTANT:
            Callers must pass *all* labels that should remain on the issue.
            Any label that is currently set on the issue but not included
            in ``labels`` will be removed.

        Note:
            - Use ``add_labels`` if you only want to add labels while keeping
              the existing ones intact.
            - Use ``update_issue_labels`` when you want to overwrite the
              complete set of labels.
        """
        pass

    @abstractmethod
    def search_issues_by_label(
        self, labels: list[str], state: str = "open"
    ) -> int | None:
        """
        Search for an issue by the given labels.

        Args:
            labels: Labels used as search conditions.
            state: Issue state to filter by (e.g. "open", "closed", "all").

        Returns:
            An issue number if at least one matching issue exists,
            otherwise None.

        Note:
            ADR-009 assumes that the combination of labels uniquely identifies
            an issue. If multiple issues match the given labels and state,
            this method returns the most recently created (highest number)
            issue to ensure deterministic behavior.
        """
        pass

    @abstractmethod
    def search_issues(self, query: str) -> list[dict[str, Any]]:
        """
        Search for issues using the GitHub search API.

        Args:
            query: The search query string.

        Returns:
            A list of matching issue objects.
        """
        pass

    @abstractmethod
    def get_issue_url(self, issue_number: int) -> str:
        """
        Return the HTML URL for the given issue number.
        """
        pass

    @abstractmethod
    def ensure_labels_exist(self, labels: list[str]) -> None:
        """
        Ensure that the given labels exist in the repository.
        If a label does not exist, it should be created with the predefined
        attributes (color, description).
        """
        pass
