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

        # Use canonical keys since Metadata handles normalization
        updates["status"] = "Approved"
        updates["date"] = today

        # Apply updates
        self.fs.update_metadata(file_path, updates)

        # 3. Move File
        moved_path_str = self.fs.safe_move_file(file_path, approved_dir)
        moved_path = Path(moved_path_str)
        print(f"Moved file to: {moved_path}")

        try:
            # 4. Create GitHub Issue
            relative_path = str(moved_path)
            content_str = doc.content

            summary = content_str[:200]
            if len(content_str) > 200:
                summary += "..."

            issue_body = (
                f"Tracking issue for approved document: {relative_path}\n\n"
                f"Original Content Summary:\n{summary}"
            )

            labels_raw = doc.metadata.get("labels")
            if not labels_raw:
                labels = ["documentation", "approved"]
            elif isinstance(labels_raw, str):
                labels = [lbl.strip() for lbl in labels_raw.split(",") if lbl.strip()]
            else:
                labels = [str(lbl).strip() for lbl in labels_raw if str(lbl).strip()]

            issue_number = self.github.create_issue(
                title=title, body=issue_body, labels=labels
            )
            print(f"Created Issue #{issue_number}")

            # 5. Update with Issue Number
            self.fs.update_metadata(moved_path, {"issue_id": issue_number})

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

        if not files:
            print("No files found in inbox.")
            return False

        processed_any = False
        for file_str in files:
            file_path = Path(file_str)
            try:
                self.process_single_file(file_path, approved_dir)
                processed_any = True
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")
                raise e  # Fail-fast as per requirements

        return processed_any
