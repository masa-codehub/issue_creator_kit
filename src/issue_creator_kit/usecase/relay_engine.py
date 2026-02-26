import logging
from datetime import UTC, datetime, timedelta
from typing import Any

from issue_creator_kit.domain.constants import RE_DEPENDENCY_ITEM
from issue_creator_kit.domain.interfaces import IGitHubAdapter
from issue_creator_kit.domain.services.metadata_parser import MetadataParser
from issue_creator_kit.domain.services.renderer import IssueRenderer

logger = logging.getLogger(__name__)


class RelayEngine:
    """
    Engine to handle task relay (ignition) and convergence (sync).
    """

    def __init__(
        self,
        github: IGitHubAdapter,
        metadata_parser: MetadataParser,
        renderer: IssueRenderer,
    ):
        """
        Initialize the RelayEngine.

        Args:
            github: Adapter for GitHub API interactions.
            metadata_parser: Service to parse task metadata from issue bodies.
            renderer: Service to render issues.
        """
        self.github = github
        self.metadata_parser = metadata_parser
        self.renderer = renderer

    def execute_relay(self, closed_issue_no: int, dry_run: bool = False) -> None:
        """
        Triggered when an issue is closed. Find descendants and update them.

        Args:
            closed_issue_no: The number of the issue that was closed.
            dry_run: If True, skip actual issue creation/modification.
        """
        # 4.1. Source Task
        source_issue = self.github.get_issue(closed_issue_no)
        source_task = self.metadata_parser.parse(source_issue["body"])

        # 4.2. Search Descendants
        # Use depends_on: "task-id" to find issues that list this task as dependency
        query = f'is:issue is:open "depends_on": "{source_task.id}"'
        descendants = self.github.search_issues(query)

        for desc in descendants:
            issue_no = desc.get("number")
            if isinstance(issue_no, int):
                try:
                    # 4.3.1. Verification (Re-verify because search might have false positives)
                    desc_body = desc.get("body") or ""
                    if not desc_body:
                        desc_issue = self.github.get_issue(issue_no)
                        desc_body = desc_issue["body"]

                    desc_task = self.metadata_parser.parse(desc_body)
                    if source_task.id not in desc_task.depends_on:
                        logger.info(
                            f"Skipping Issue #{issue_no}: source task {source_task.id} not in metadata depends_on."
                        )
                        continue

                    self._process_issue(issue_no, dry_run=dry_run)
                except Exception as e:
                    logger.error(f"Failed to process descendant issue #{issue_no}: {e}")

    def execute_sync(
        self, label: str = "task", dry_run: bool = False
    ) -> dict[str, int]:
        """
        Bulk sync all issues with the given label.

        Args:
            label: The label to search for (default: "task").
            dry_run: If True, skip actual issue creation/modification.

        Returns:
            A summary of the sync results (success, skipped, failed).
        """
        # 1. Bulk Fetch (Include updated filter for scalability)
        one_month_ago = (datetime.now(UTC) - timedelta(days=30)).strftime("%Y-%m-%d")
        query = f"is:issue label:{label} updated:>={one_month_ago}"
        all_issues = self.github.search_issues(query)

        # 2. State Cache
        state_cache: dict[int, str] = {}
        for issue in all_issues:
            issue_no = issue.get("number")
            state = issue.get("state")
            if isinstance(issue_no, int) and isinstance(state, str):
                state_cache[issue_no] = state

        results = {"success": 0, "skipped": 0, "failed": 0}

        # 3. Process Open Issues
        for issue in all_issues:
            issue_no = issue.get("number")
            if not isinstance(issue_no, int):
                continue

            if issue.get("state") != "open":
                results["skipped"] += 1
                continue

            try:
                self._process_issue(issue_no, state_cache=state_cache, dry_run=dry_run)
                results["success"] += 1
            except Exception as e:
                logger.error(f"Failed to process issue #{issue_no}: {e}")
                results["failed"] += 1

        return results

    def _process_issue(
        self,
        issue_no: int,
        state_cache: dict[int, str] | None = None,
        dry_run: bool = False,
    ) -> None:
        """
        Verify, update checklist, and check for ignition.

        Args:
            issue_no: The issue number to process.
            state_cache: Optional cache of issue states.
        """
        issue = self.github.get_issue(issue_no)
        body = issue["body"]
        labels_val: Any = issue.get("labels", [])
        current_labels: list[str] = labels_val if isinstance(labels_val, list) else []
        task = self.metadata_parser.parse(body)

        id_map = self._parse_dependencies_from_body(body)

        completed_nos: set[int] = set()
        all_closed = True

        for dep_id in task.depends_on:
            dep_issue_no = id_map.get(dep_id)
            if not dep_issue_no:
                # If Task ID cannot be resolved, we can't confirm it's closed
                all_closed = False
                continue

            # Use cache or fetch
            state = None
            if state_cache and dep_issue_no in state_cache:
                state = state_cache[dep_issue_no]
            else:
                try:
                    dep_issue = self.github.get_issue(dep_issue_no)
                    state = dep_issue.get("state")
                except Exception:
                    state = "unknown"

            if state == "closed":
                completed_nos.add(dep_issue_no)
            else:
                all_closed = False

        # Update Checklist
        rendered = self.renderer.render(task, id_map, completed_issue_nos=completed_nos)

        if rendered.body != body:
            if dry_run:
                logger.info(f"[DRY-RUN] Would update body of issue #{issue_no}")
            else:
                self.github.patch_issue(issue_no, rendered.body)

        # Ignition: Add gemini label if all dependencies are closed
        # and the label is not already present on GitHub.
        if all_closed and "gemini" not in current_labels:
            if dry_run:
                logger.info(f"[DRY-RUN] Would add 'gemini' label to issue #{issue_no}")
            else:
                self.github.add_labels(issue_no, ["gemini"])

    def _parse_dependencies_from_body(self, body: str) -> dict[str, int]:
        """
        Extract Task ID -> Issue No mapping from ## Dependencies section.

        Args:
            body: The issue body content.

        Returns:
            A mapping from Task ID to Issue Number.
        """
        matches = RE_DEPENDENCY_ITEM.findall(body)
        return {task_id: int(issue_no) for issue_no, task_id in matches}
