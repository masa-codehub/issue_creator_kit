import logging
import re

from issue_creator_kit.domain.exceptions import GitHubAPIError
from issue_creator_kit.domain.interfaces import IGitHubAdapter

logger = logging.getLogger(__name__)


class L1SyncService:
    """Service to synchronize L1 issue checklist with real issue numbers."""

    def __init__(self, github: IGitHubAdapter):
        self.github = github

    def sync_checklist(self, l1_id: int, in_memory_map: dict[str, int]) -> int:
        """
        Fetch L1 issue, replace temporary IDs with #number, and patch back.
        Returns the number of IDs replaced.
        """
        try:
            issue = self.github.get_issue(l1_id)
            body = issue.get("body", "")

            new_body = body
            # Sort IDs by length descending to avoid substring replacement issues
            sorted_ids = sorted(in_memory_map.keys(), key=len, reverse=True)

            replace_count = 0
            for task_id in sorted_ids:
                issue_no = in_memory_map[task_id]
                # Regex for checklist-aware replacement: (- [[ xX]]\s+)(task-id)(?!\w)
                pattern = rf"(- \[[ xX]\]\s+)({re.escape(task_id)})(?!\w)"
                new_body, num_replacements = re.subn(
                    pattern, rf"\1#{issue_no}", new_body
                )
                replace_count += num_replacements

            self.github.patch_issue(l1_id, new_body)
            logger.info(
                f"L1 issue #{l1_id} checklist synchronized with {replace_count} replacements."
            )
            return replace_count

        except GitHubAPIError as e:
            logger.error(f"Failed to sync L1 issue #{l1_id}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error syncing L1 issue #{l1_id}: {e}")
            raise
