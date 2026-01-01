import os
from typing import Any

import requests


class GitHubAdapter:
    def __init__(self, token: str | None = None, repo: str | None = None):
        self.token = (
            token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        )
        self.repo = repo or os.environ.get("GITHUB_REPOSITORY")

        if not self.token or not self.repo:
            # We allow initialization without credentials, but methods will fail
            pass

    def _get_headers(self) -> dict[str, str]:
        if not self.token:
            raise ValueError("GitHub token is not set.")
        return {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
        }

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

        if response.status_code == 201:
            return response.json()["number"]
        raise RuntimeError(
            f"Failed to create issue. Status: {response.status_code}, Body: {response.text}"
        )

    # Future: Add more methods as needed (e.g. get_issue, comment, etc.)
