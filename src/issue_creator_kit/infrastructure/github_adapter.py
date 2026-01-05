import os
from typing import Any

import requests


class GitHubAdapter:
    def __init__(self, token: str | None = None, repo: str | None = None):
        self.token = (
            token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        )
        self.repo = repo or os.environ.get("GITHUB_REPOSITORY")

        if not self.token:
            raise ValueError("GitHub token is required.")
        if not self.repo:
            # Repo might be optional for some operations?
            # But usually needed. Let's not break if repo missing unless strictly required?
            # Reviewer specifically mentioned Token.
            # But let's check token.
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

    def create_pull_request(
        self, title: str, body: str, head: str, base: str = "main"
    ) -> str:
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

        if response.status_code == 201:
            return response.json()["html_url"]
        raise RuntimeError(
            f"Failed to create PR. Status: {response.status_code}, Body: {response.text}"
        )

    # Future: Add more methods as needed (e.g. get_issue, comment, etc.)
