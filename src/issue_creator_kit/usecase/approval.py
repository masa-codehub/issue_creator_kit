# ruff: noqa: T201
from datetime import datetime
from pathlib import Path

from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter


class ApprovalUseCase:
    def __init__(self, fs_adapter: FileSystemAdapter, github_adapter: GitHubAdapter):
        self.fs = fs_adapter
        self.github = github_adapter

    def process_single_file(self, file_path: Path, approved_dir: Path) -> None:
        """
        承認されたドキュメントを処理します。
        """
        print(f"Processing approval for: {file_path}")

        # 1. Load Document
        doc = self.fs.read_document(file_path)
        title = (
            doc.metadata.get("title") or doc.metadata.get("タイトル") or file_path.stem
        )

        # 2. Update Status and Date
        today = datetime.now().strftime("%Y-%m-%d")
        updates = {}

        # Check keys to maintain compatibility
        keys_to_check = [
            "Status",
            "status",
            "Date",
            "date",
            "Last Updated",
            "last_updated",
        ]

        # Simple heuristic: Update status if key exists, or default to "Status"
        status_key = next(
            (k for k in keys_to_check if k in doc.metadata and "status" in k.lower()),
            "Status",
        )
        date_key = next(
            (k for k in keys_to_check if k in doc.metadata and "date" in k.lower()),
            "Date",
        )

        updates[status_key] = "承認済み"
        updates[date_key] = today

        # Apply updates
        self.fs.update_metadata(file_path, updates)

        # 3. Move File
        moved_path = self.fs.safe_move_file(file_path, approved_dir)
        print(f"Moved file to: {moved_path}")

        try:
            # 4. Create GitHub Issue
            # Re-read doc from moved path to get latest content (though content obj is same)
            # Actually we can just use the content string we have in memory + updates

            relative_path = str(moved_path)
            content_str = doc.content

            summary = content_str[:200]
            if len(content_str) > 200:
                summary += "..."

            issue_body = (
                f"Tracking issue for approved document: {relative_path}\n\n"
                f"Original Content Summary:\n{summary}"
            )

            labels_raw = (
                doc.metadata.get("labels")
                or doc.metadata.get("ラベル")
                or ["documentation", "approved"]
            )
            labels = []
            if isinstance(labels_raw, str):
                labels = [lbl.strip() for lbl in labels_raw.split(",") if lbl.strip()]
            elif isinstance(labels_raw, list):
                labels = [
                    lbl.strip()
                    for lbl in labels_raw
                    if isinstance(lbl, str) and lbl.strip()
                ]

            issue_number = self.github.create_issue(
                title=title, body=issue_body, labels=labels
            )
            print(f"Created Issue #{issue_number}")

            # 5. Update with Issue Number
            self.fs.update_metadata(moved_path, {"Issue": f"#{issue_number}"})
            # Also update lower case key if it exists
            if "issue" in doc.metadata:
                self.fs.update_metadata(moved_path, {"issue": f"#{issue_number}"})

            print(f"Updated document with Issue #{issue_number}")

        except Exception as e:
            # Rollback
            print(f"Error during Issue creation: {e}")
            try:
                self.fs.safe_move_file(moved_path, file_path.parent, overwrite=True)
                print(f"Rolled back file move to: {file_path}")
            except Exception as rollback_error:
                print(f"Failed to rollback file move: {rollback_error}")
            raise e

    def process_all_files(self, inbox_dir: Path, approved_dir: Path) -> bool:
        files = self.fs.list_files(inbox_dir)
        files = [f for f in files if f.is_file()]

        if not files:
            print("No files found in inbox.")
            return False

        processed_any = False
        for file_path in files:
            try:
                self.process_single_file(file_path, approved_dir)
                processed_any = True
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
                raise e  # Fail-fast as per requirements

        return processed_any
