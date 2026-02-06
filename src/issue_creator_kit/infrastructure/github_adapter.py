import json
import os
from typing import Any

import requests

from issue_creator_kit.domain.document import Document
from issue_creator_kit.domain.exceptions import (
    GitHubAPIError,
    GitHubRateLimitError,
)
from issue_creator_kit.domain.interfaces import IGitHubAdapter


class GitHubAdapter(IGitHubAdapter):
    def __init__(self, token: str | None = None, repo: str | None = None):
        self.token = (
            token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        )
        self.repo = repo or os.environ.get("GITHUB_REPOSITORY")

        if not self.token:
            raise ValueError("GitHub token is required.")

    def _get_headers(self) -> dict[str, str]:
        if not self.token:
            raise ValueError("GitHub token is not set.")
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

    def _handle_response(self, response: requests.Response) -> requests.Response:
        remaining = response.headers.get("X-RateLimit-Remaining")
        is_rate_limit = response.status_code == 429 or (
            response.status_code == 403
            and (
                (remaining is not None and int(remaining) == 0)
                or "rate limit" in response.text.lower()
            )
        )
        if is_rate_limit:
            raise GitHubRateLimitError(
                f"GitHub API Rate Limit exceeded: {response.text}",
                status_code=response.status_code,
            )
        if 400 <= response.status_code < 600:
            raise GitHubAPIError(
                f"GitHub API Error: {response.status_code} - {response.text}",
                status_code=response.status_code,
            )
        return response

    def create_issue(
        self, title: str, body: str, labels: list[str] | None = None
    ) -> int:
        if not self.repo:
            raise ValueError("GitHub repository is not set.")

        api_url = f"https://api.github.com/repos/{self.repo}/issues"
        data: dict[str, Any] = {
            "title": title,
            "body": body,
        }
        if labels:
            data["labels"] = labels

        response = requests.post(api_url, headers=self._get_headers(), json=data)
        self._handle_response(response)

        return response.json()["number"]

    def find_or_create_issue(
        self, title: str, body: str, labels: list[str] | None = None
    ) -> int:
        """
        Find an existing open issue with the same title or create a new one.

        This method searches open issues in the configured repository whose
        title matches the given ``title``. If at least one matching issue is
        found, the most recently created issue number is returned. If no
        matching issue exists, a new issue is created with the provided
        ``title``, ``body``, and optional ``labels``.

        Args:
            title: Title of the issue to search for or create.
            body: Body (description) of the issue to create when no existing
                matching issue is found.
            labels: Optional list of labels to apply when creating a new issue.

        Returns:
            int: The GitHub issue number of the existing or newly created issue.

        Raises:
            ValueError: If the GitHub repository is not configured.
            GitHubAPIError: If the GitHub API returns an error response.
            GitHubRateLimitError: If the GitHub API rate limit has been exceeded.
        """
        if not self.repo:
            raise ValueError("GitHub repository is not set.")

        # Search for existing open issue with the same title
        # Escape special characters in title for GitHub search query
        special_chars = '\\"[]():'
        escaped_title = "".join(f"\\{c}" if c in special_chars else c for c in title)

        query = f'is:issue is:open in:title "{escaped_title}" repo:{self.repo}'
        api_url = "https://api.github.com/search/issues"
        params = {"q": query, "sort": "created", "order": "desc"}

        response = requests.get(api_url, headers=self._get_headers(), params=params)
        self._handle_response(response)

        items = response.json().get("items", [])
        if not isinstance(items, list):
            items = []

        # Ensure exact title match and correct type
        matching_items = [
            item
            for item in items
            if isinstance(item, dict)
            and item.get("title") == title
            and isinstance(item.get("number"), int)
        ]

        if matching_items:
            # Sort by created_at desc just in case
            matching_items.sort(
                key=lambda x: x.get("created_at") or "",
                reverse=True,
            )
            return matching_items[0]["number"]

        return self.create_issue(title, body, labels)

    def create_pull_request(
        self, title: str, body: str, head: str, base: str
    ) -> tuple[str, int]:
        """
        Create a pull request and return its URL and number.
        """
        if not self.repo:
            raise ValueError("GitHub repository is not set.")

        api_url = f"https://api.github.com/repos/{self.repo}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base,
        }

        response = requests.post(api_url, headers=self._get_headers(), json=data)
        self._handle_response(response)

        res_data = response.json()
        return res_data["html_url"], res_data["number"]

    def add_labels(self, issue_number: int, labels: list[str]) -> None:
        """
        Add labels to an issue or pull request.
        """
        if not self.repo:
            raise ValueError("GitHub repository is not set.")

        api_url = (
            f"https://api.github.com/repos/{self.repo}/issues/{issue_number}/labels"
        )
        data = {"labels": labels}

        response = requests.post(api_url, headers=self._get_headers(), json=data)
        self._handle_response(response)

    def add_comment(self, issue_number: int, body: str) -> None:
        """
        Add a comment to an issue or pull request.
        """
        if not self.repo:
            raise ValueError("GitHub repository is not set.")

        api_url = (
            f"https://api.github.com/repos/{self.repo}/issues/{issue_number}/comments"
        )
        data = {"body": body}

        response = requests.post(api_url, headers=self._get_headers(), json=data)
        self._handle_response(response)

    def sync_issue(self, doc: Document) -> int:
        """
        Sync a document's state to a GitHub issue.
        Creates a new issue or updates an existing one based on metadata.
        """
        if not self.repo:
            raise ValueError("GitHub repository is not set.")

        # 1. Map Title: id + ": " + (title)
        task_id = doc.metadata.id
        title_raw = doc.metadata.get("title") or ""
        title = f"{task_id}: {title_raw}"

        # 2. Map Body: content + metadata table
        metadata_table = "\n\n| Key | Value |\n| :--- | :--- |\n"
        relevant_keys = ["id", "status", "phase", "type", "depends_on", "parent"]
        for key in relevant_keys:
            val = doc.metadata.get(key)
            if val is not None:
                # Format lists/dicts as JSON strings for better readability
                val_str = json.dumps(val) if isinstance(val, list | dict) else str(val)
                # Escape pipe characters for markdown table integrity
                val_str = val_str.replace("|", "\\|")
                metadata_table += f"| {key} | {val_str} |\n"
        body = doc.content + metadata_table

        # 3. Map Labels
        labels = []
        if doc.metadata.phase:
            labels.append(doc.metadata.phase)
        if doc.metadata.type:
            labels.append(doc.metadata.type)

        # 4. Sync logic
        issue_id = doc.metadata.issue_id
        if issue_id:
            # Update existing
            api_url = f"https://api.github.com/repos/{self.repo}/issues/{issue_id}"
            data = {"title": title, "body": body, "labels": labels}
            response = requests.patch(api_url, headers=self._get_headers(), json=data)
            self._handle_response(response)
            return issue_id

        # Search or Create
        return self.find_or_create_issue(title, body, labels)
