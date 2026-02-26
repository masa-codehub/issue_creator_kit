import copy
import json
import logging
import os
import re
import time
from collections.abc import Callable
from datetime import UTC, datetime
from functools import wraps
from typing import Any

import requests

from issue_creator_kit.domain.document import Document
from issue_creator_kit.domain.exceptions import (
    GitHubAPIError,
    GitHubRateLimitError,
)
from issue_creator_kit.domain.interfaces import IGitHubAdapter
from issue_creator_kit.domain.models.document import (
    TASK_ID_PATTERN,
)

logger = logging.getLogger(__name__)


def require_repo(func: Callable[..., Any]) -> Callable[..., Any]:
    @wraps(func)
    def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
        if not self.repo:
            raise ValueError("GitHub repository is not set.")
        return func(self, *args, **kwargs)

    return wrapper


class GitHubAdapter(IGitHubAdapter):
    # Retry Policy
    MAX_RETRIES = 3
    INITIAL_BACKOFF = 5
    BACKOFF_FACTOR = 2

    # Pagination
    PER_PAGE = 100
    MAX_PAGES = 10

    # Label Attributes
    LABEL_ATTRIBUTES = {
        "L1": {
            "color": "d4c5f9",
            "description": "ADRに対応する最上位管理Issueであることを示す階層ラベル。",
        },
    }
    ADR_LABEL_PATTERN = re.compile(r"^adr:(\d{3})$")
    ADR_LABEL_COLOR = "0052cc"
    ADR_LABEL_DESCRIPTION = (
        "ADR IDを一意に識別する。`{NNN}` は3桁ゼロ埋めの数値（例: `adr:009`）。"
    )

    def __init__(self, token: str | None = None, repo: str | None = None):
        self.token = (
            token or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
        )
        self.repo = repo or os.environ.get("GITHUB_REPOSITORY")

        if not self.token:
            raise ValueError("GitHub token is required.")

        # Session cache for search results
        self._search_cache: dict[str, list[dict[str, Any]]] = {}

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

    def _execute_with_retry(
        self, func: Callable[[], requests.Response]
    ) -> requests.Response:
        """
        Execute a request function with exponential backoff retry.
        Policy: Max 3 retries, initial 5s, exponential factor 2.
        """
        backoff = self.INITIAL_BACKOFF
        for attempt in range(self.MAX_RETRIES + 1):
            try:
                response = func()
                return self._handle_response(response)
            except GitHubRateLimitError:
                if attempt < self.MAX_RETRIES:
                    logger.warning(
                        f"Rate limit hit. Retrying in {backoff} seconds... "
                        f"(Retry {attempt + 1}/{self.MAX_RETRIES})"
                    )
                    time.sleep(backoff)
                    backoff *= self.BACKOFF_FACTOR
                else:
                    raise
        # Should not reach here
        raise GitHubAPIError("Unexpected retry failure")

    @require_repo
    def create_issue(
        self,
        title: str,
        body: str,
        labels: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> int:
        # Metadata Injection
        if metadata:
            # Work on a copy to avoid mutating the caller's metadata dict
            metadata_for_comment = dict(metadata)

            # Auto-inject timestamp if missing
            if "injected_at" not in metadata_for_comment:
                metadata_for_comment["injected_at"] = datetime.now(UTC).strftime(
                    "%Y-%m-%dT%H:%M:%SZ"
                )

            metadata_json = json.dumps(metadata_for_comment)
            # Safety check against HTML comment injection
            if "-->" in metadata_json or "<!--" in metadata_json:
                raise ValueError(
                    "Metadata contains unsafe sequence for HTML comment injection."
                )

            body += f"\n\n<!-- metadata:{metadata_json} -->"

        api_url = f"https://api.github.com/repos/{self.repo}/issues"
        data: dict[str, Any] = {
            "title": title,
            "body": body,
        }
        if labels:
            data["labels"] = labels

        def do_create() -> requests.Response:
            return requests.post(api_url, headers=self._get_headers(), json=data)

        response = self._execute_with_retry(do_create)

        return response.json()["number"]

    @require_repo
    def find_issue_by_title(self, title: str) -> int | None:
        """
        Find an existing open issue with the same title.
        """
        # Search for existing open issue with the same title
        special_chars = '\\"[]():'
        escaped_title = "".join(f"\\{c}" if c in special_chars else c for c in title)

        query = f'is:issue is:open in:title "{escaped_title}" repo:{self.repo}'
        api_url = "https://api.github.com/search/issues"
        params = {"q": query, "sort": "created", "order": "desc"}

        def do_search() -> requests.Response:
            return requests.get(api_url, headers=self._get_headers(), params=params)

        response = self._execute_with_retry(do_search)

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

        return None

    @require_repo
    def find_or_create_issue(
        self, title: str, body: str, labels: list[str] | None = None
    ) -> int:
        """
        Find an existing open issue with the same title or create a new one.
        """
        issue_no = self.find_issue_by_title(title)
        if issue_no:
            return issue_no

        return self.create_issue(title, body, labels)

    @require_repo
    def create_pull_request(
        self, title: str, body: str, head: str, base: str
    ) -> tuple[str, int]:
        """
        Create a pull request and return its URL and number.
        """
        api_url = f"https://api.github.com/repos/{self.repo}/pulls"
        data = {
            "title": title,
            "body": body,
            "head": head,
            "base": base,
        }

        def do_create_pr() -> requests.Response:
            return requests.post(api_url, headers=self._get_headers(), json=data)

        response = self._execute_with_retry(do_create_pr)

        res_data = response.json()
        return res_data["html_url"], res_data["number"]

    @require_repo
    def get_issue(self, issue_number: int) -> dict[str, Any]:
        """
        Get details of a specific issue.
        """
        api_url = f"https://api.github.com/repos/{self.repo}/issues/{issue_number}"

        def do_get() -> requests.Response:
            return requests.get(api_url, headers=self._get_headers())

        response = self._execute_with_retry(do_get)
        data = response.json()
        etag = response.headers.get("ETag")

        if not etag:
            raise GitHubAPIError(
                f"ETag header is missing in response for issue {issue_number}",
                status_code=response.status_code,
            )

        # Normalize null body to empty string
        body = data.get("body") or ""
        state = data.get("state") or "unknown"
        labels = [lbl["name"] for lbl in data.get("labels", []) if "name" in lbl]

        return {"body": body, "etag": etag, "state": state, "labels": labels}

    @require_repo
    def patch_issue(self, issue_number: int, body: str) -> None:
        """
        Update an issue body.
        """
        api_url = f"https://api.github.com/repos/{self.repo}/issues/{issue_number}"
        data = {"body": body}
        headers = self._get_headers()

        def do_patch() -> requests.Response:
            return requests.patch(api_url, headers=headers, json=data)

        self._execute_with_retry(do_patch)

    @require_repo
    def add_labels(self, issue_number: int, labels: list[str]) -> None:
        """
        Add labels to an issue or pull request.
        """
        api_url = (
            f"https://api.github.com/repos/{self.repo}/issues/{issue_number}/labels"
        )
        data = {"labels": labels}

        def do_add_labels() -> requests.Response:
            return requests.post(api_url, headers=self._get_headers(), json=data)

        self._execute_with_retry(do_add_labels)

    @require_repo
    def add_comment(self, issue_number: int, body: str) -> None:
        """
        Add a comment to an issue or pull request.
        """
        api_url = (
            f"https://api.github.com/repos/{self.repo}/issues/{issue_number}/comments"
        )
        data = {"body": body}

        def do_add_comment() -> requests.Response:
            return requests.post(api_url, headers=self._get_headers(), json=data)

        self._execute_with_retry(do_add_comment)

    @require_repo
    def search_issues_by_label(
        self, labels: list[str], state: str = "open"
    ) -> int | None:
        """
        Search for an issue by labels with pagination.
        """
        if not labels:
            raise ValueError("Labels are required for search.")

        api_url = f"https://api.github.com/repos/{self.repo}/issues"
        params: dict[str, str | int] = {
            "labels": ",".join(labels),
            "state": state,
            "sort": "created",
            "direction": "desc",
            "per_page": self.PER_PAGE,
        }

        all_issues: list[dict[str, Any]] = []
        page_count = 0

        next_url: str | None = api_url

        while next_url and page_count < self.MAX_PAGES:
            current_url = next_url

            def fetch_page(url: str = current_url) -> requests.Response:
                return requests.get(
                    url,
                    headers=self._get_headers(),
                    params=params if url == api_url else None,
                )

            response = self._execute_with_retry(fetch_page)

            issues = response.json()
            if not isinstance(issues, list):
                raise GitHubAPIError(
                    f"Unexpected GitHub API response type for issues: {type(issues).__name__}"
                )

            all_issues.extend(issues)
            page_count += 1

            # Pagination logic
            next_url = None
            if response.links and "next" in response.links:
                next_url = response.links["next"]["url"]

        if not all_issues:
            return None

        # Pick the largest issue number (A-02), excluding PRs
        issue_numbers = [
            issue["number"]
            for issue in all_issues
            if isinstance(issue, dict)
            and isinstance(issue.get("number"), int)
            and "pull_request" not in issue
        ]

        if not issue_numbers:
            return None

        if len(issue_numbers) > 1:
            logger.warning(
                f"Multiple issues found for labels {labels}: {issue_numbers}. "
                "Using the largest number as the canonical issue."
            )

        return max(issue_numbers)

    @require_repo
    def search_issues(self, query: str) -> list[dict[str, Any]]:
        """
        Search for issues using the GitHub search API.
        Implements Metadata ID priority and session caching.
        """
        # --- 1. Task ID Priority Logic ---
        if TASK_ID_PATTERN.match(query):
            # 1.1. Metadata ID Search (Priority)
            # Query format: "\"id\": \"task-XXX-NN\"" in:body is:issue
            # Outer quotes are required for exact phrase matching in GitHub API
            metadata_phrase = f'\\"id\\": \\"{query}\\"'
            metadata_query = f'"{metadata_phrase}" in:body is:issue'
            results = self._search_issues_raw(metadata_query)
            if results:
                return results

            # 1.2. Label Search (Fallback)
            # extract ADR number from task-XXX-NN -> adr:XXX
            # Use regex to find the 3-digit ADR number after 'task-'
            adr_match = re.search(r"task-(\d{3})-", query)
            if adr_match:
                adr_num = adr_match.group(1)
                # Narrow fallback search to issues under the ADR that also contain the specific task ID in the body
                label_query = f'"{query}" in:body label:task label:adr:{adr_num}'
                return self._search_issues_raw(label_query)

        # --- 2. Generic Search ---
        return self._search_issues_raw(query)

    def _search_issues_raw(self, query: str) -> list[dict[str, Any]]:
        """
        Internal raw search with session caching.
        """
        # Always scope to the current repo and ensure it's an issue
        if "is:issue" not in query:
            query = f"{query} is:issue"
        if f"repo:{self.repo}" not in query:
            final_query = f"{query} repo:{self.repo}"
        else:
            final_query = query

        # Cache Check (Return deep copy to prevent mutation side-effects)
        if final_query in self._search_cache:
            logger.debug(f"Search cache hit: {final_query}")
            return copy.deepcopy(self._search_cache[final_query])

        api_url = "https://api.github.com/search/issues"
        params: dict[str, str | int] = {
            "q": final_query,
            "sort": "created",
            "order": "desc",
            "per_page": self.PER_PAGE,
        }

        all_issues: list[dict[str, Any]] = []
        page_count = 0
        next_url: str | None = api_url

        while next_url and page_count < self.MAX_PAGES:
            current_url = next_url

            def fetch_page(url: str = current_url) -> requests.Response:
                return requests.get(
                    url,
                    headers=self._get_headers(),
                    params=params if url == api_url else None,
                )

            response = self._execute_with_retry(fetch_page)
            data = response.json()
            items = data.get("items", [])
            if not isinstance(items, list):
                break

            all_issues.extend(items)
            page_count += 1

            next_url = None
            if response.links and "next" in response.links:
                next_url = response.links["next"]["url"]

        # Filter out pull requests (Safety check if is:issue filter wasn't enough)
        results = [issue for issue in all_issues if "pull_request" not in issue]

        # Store to cache (Store deep copy to prevent mutation side-effects)
        self._search_cache[final_query] = copy.deepcopy(results)
        return results

    @require_repo
    def get_issue_url(self, issue_number: int) -> str:
        """
        Return the HTML URL for the given issue number.
        """
        return f"https://github.com/{self.repo}/issues/{issue_number}"

    @require_repo
    def sync_issue(self, doc: Document) -> int:
        """
        Sync a document's state to a GitHub issue.
        Creates a new issue or updates an existing one based on metadata.
        """
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

            def do_patch() -> requests.Response:
                return requests.patch(api_url, headers=self._get_headers(), json=data)

            self._execute_with_retry(do_patch)
            return issue_id

        # Search or Create
        return self.find_or_create_issue(title, body, labels)

    @require_repo
    def ensure_labels_exist(self, labels: list[str]) -> None:
        """
        Ensure that the given labels exist in the repository.
        If a label does not exist, it should be created with the predefined
        attributes (color, description).
        """
        for label_name in labels:
            attrs = self._get_label_attributes(label_name)
            if not attrs:
                logger.debug(f"Skipping unknown label: {label_name}")
                continue

            api_url = f"https://api.github.com/repos/{self.repo}/labels"
            data = {
                "name": label_name,
                "color": attrs["color"],
                "description": attrs["description"],
            }

            def do_create_label(
                url: str = api_url, payload: dict[str, Any] = data
            ) -> requests.Response:
                return requests.post(url, headers=self._get_headers(), json=payload)

            try:
                self._execute_with_retry(do_create_label)
                logger.info(f"Label created: {label_name}")
            except GitHubAPIError as e:
                if e.status_code == 422:
                    # Prefer checking the structured error code over string matching.
                    try:
                        # Extract JSON part from error message "GitHub API Error: 422 - {..."
                        error_body = e.message.split(" - ", 1)[-1]
                        error_data = json.loads(error_body)
                        is_already_exists = any(
                            err.get("code") == "already_exists"
                            for err in error_data.get("errors", [])
                        )
                    except (json.JSONDecodeError, IndexError):
                        # Fallback to string matching if parsing fails.
                        is_already_exists = "already_exists" in e.message.lower()

                    if is_already_exists:
                        logger.debug(f"Label already exists: {label_name}")
                    else:
                        raise
                else:
                    raise

    def _get_label_attributes(self, label_name: str) -> dict[str, str] | None:
        """
        Map label name to color and description.
        """
        # 1. Static mapping
        if label_name in self.LABEL_ATTRIBUTES:
            return self.LABEL_ATTRIBUTES[label_name]

        # 2. Pattern-based mapping (adr:{NNN})
        match = self.ADR_LABEL_PATTERN.match(label_name)
        if match:
            return {
                "color": self.ADR_LABEL_COLOR,
                "description": f"ADR ID {match.group(1)} を一意に識別するためのラベル。",
            }

        return None
