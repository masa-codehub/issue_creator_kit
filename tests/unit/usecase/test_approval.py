from pathlib import Path
from unittest.mock import Mock

import pytest

from issue_creator_kit.domain.document import Document
from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter
from issue_creator_kit.usecase.approval import ApprovalUseCase


class TestApprovalUseCase:
    @pytest.fixture
    def mocks(self):
        fs_adapter = Mock(spec=FileSystemAdapter)
        github_adapter = Mock(spec=GitHubAdapter)
        return fs_adapter, github_adapter

    def test_process_single_file_success(self, mocks):
        """
        Given: A valid document
        When: process_single_file is called
        Then:
         1. Document is read
         2. Metadata (Status, Date) updated
         3. File moved to approved_dir
         4. Issue created via GitHubAdapter
         5. Metadata (Issue) updated
        """
        fs_adapter, github_adapter = mocks
        usecase = ApprovalUseCase(fs_adapter, github_adapter)

        # Setup
        file_path = Path("inbox/doc.md")
        approved_dir = Path("approved")
        moved_path = approved_dir / "doc.md"

        doc_mock = Mock(spec=Document)
        doc_mock.content = "Test content"
        doc_mock.metadata = {"title": "Test Doc", "labels": "task, P1"}

        fs_adapter.read_document.return_value = doc_mock
        fs_adapter.safe_move_file.return_value = moved_path
        github_adapter.create_issue.return_value = 123

        # Execute
        usecase.process_single_file(file_path, approved_dir)

        # Verify
        fs_adapter.read_document.assert_called_once_with(file_path)

        # Verify initial metadata update (Status, Date)
        # Note: We can't easily verify the exact date since it uses datetime.now()
        # So we check if update_metadata was called with expected keys.
        update_calls = fs_adapter.update_metadata.call_args_list
        assert len(update_calls) == 2

        # First update: Status and Date
        first_call_args = update_calls[0]
        assert first_call_args[0][0] == file_path
        updates_1 = first_call_args[0][1]
        assert "Status" in updates_1
        assert updates_1["Status"] == "承認済み"
        assert "Date" in updates_1

        # Move file
        fs_adapter.safe_move_file.assert_called_once_with(file_path, approved_dir)

        # Create Issue
        github_adapter.create_issue.assert_called_once()
        _, kwargs = github_adapter.create_issue.call_args
        assert kwargs["title"] == "Test Doc"
        assert "Tracking issue for approved document" in kwargs["body"]
        assert kwargs["labels"] == ["task", "P1"]

        # Second update: Issue number
        second_call_args = update_calls[1]
        assert second_call_args[0][0] == moved_path
        updates_2 = second_call_args[0][1]
        assert updates_2["Issue"] == "#123"

    def test_process_single_file_variants(self, mocks):
        """
        Given: Document with list labels and lowercase 'issue' key
        When: process_single_file is called
        Then:
         1. Labels are correctly processed from list
         2. Lowercase 'issue' key is also updated
        """
        fs_adapter, github_adapter = mocks
        usecase = ApprovalUseCase(fs_adapter, github_adapter)

        file_path = Path("inbox/doc.md")
        approved_dir = Path("approved")
        moved_path = approved_dir / "doc.md"

        doc_mock = Mock(spec=Document)
        doc_mock.content = "Test content"
        # Test list labels and lowercase issue key presence
        doc_mock.metadata = {
            "title": "Test Doc",
            "labels": ["A", "B "],
            "issue": "#111",
        }

        fs_adapter.read_document.return_value = doc_mock
        fs_adapter.safe_move_file.return_value = moved_path
        github_adapter.create_issue.return_value = 124

        usecase.process_single_file(file_path, approved_dir)

        # Verify labels passed to GitHub
        _, kwargs = github_adapter.create_issue.call_args
        assert kwargs["labels"] == ["A", "B"]

        # Verify lowercase issue update
        # fs.update_metadata call args are (path, dict)
        # We look for the call that updates 'issue' (lowercase)
        calls = fs_adapter.update_metadata.call_args_list
        # Expecting calls:
        # 1. Status/Date
        # 2. Issue (Capitalized)
        # 3. issue (Lowercase)
        assert len(calls) == 3
        lowercase_update = calls[2]
        assert lowercase_update[0][0] == moved_path
        assert lowercase_update[0][1] == {"issue": "#124"}

    def test_process_single_file_long_content(self, mocks):
        """
        Given: Document with content > 200 chars
        When: process_single_file is called
        Then: Issue body summary is truncated with "..."
        """
        fs_adapter, github_adapter = mocks
        usecase = ApprovalUseCase(fs_adapter, github_adapter)

        file_path = Path("inbox/doc.md")
        approved_dir = Path("approved")

        doc_mock = Mock(spec=Document)
        doc_mock.content = "a" * 201
        doc_mock.metadata = {"title": "T"}
        fs_adapter.read_document.return_value = doc_mock
        fs_adapter.safe_move_file.return_value = approved_dir / "doc.md"
        github_adapter.create_issue.return_value = 1

        usecase.process_single_file(file_path, approved_dir)

        _, kwargs = github_adapter.create_issue.call_args
        assert "..." in kwargs["body"]
        assert "Original Content Summary" in kwargs["body"]

    def test_process_single_file_rollback_failure(self, mocks):
        """
        Given: Issue creation fails AND Rollback fails
        When: process_single_file is called
        Then:
         1. Rollback exception is caught and printed (swallowed in a way, but original exception re-raised)
         2. Original exception is raised
        """
        fs_adapter, github_adapter = mocks
        usecase = ApprovalUseCase(fs_adapter, github_adapter)

        file_path = Path("inbox/doc.md")
        approved_dir = Path("approved")

        doc_mock = Mock(spec=Document)
        doc_mock.content = "content"
        doc_mock.metadata = {"title": "T"}
        fs_adapter.read_document.return_value = doc_mock
        fs_adapter.safe_move_file.return_value = approved_dir / "doc.md"

        # 1. Issue creation fails
        github_adapter.create_issue.side_effect = RuntimeError("Issue Error")

        # 2. Rollback fails
        # The second call to safe_move_file (rollback) should fail
        # safe_move_file is called: 1. move to approved, 2. move back (rollback)
        fs_adapter.safe_move_file.side_effect = [
            approved_dir / "doc.md",
            RuntimeError("Rollback Error"),
        ]

        with pytest.raises(RuntimeError, match="Issue Error"):
            usecase.process_single_file(file_path, approved_dir)

        # Verify safe_move_file was called twice (move + rollback attempt)
        assert fs_adapter.safe_move_file.call_count == 2

    def test_process_single_file_rollback(self, mocks):
        """
        Given: GitHub issue creation fails
        When: process_single_file is called
        Then:
         1. Exception is raised
         2. File move is rolled back (safe_move_file called with overwrite=True to original parent)
        """
        fs_adapter, github_adapter = mocks
        usecase = ApprovalUseCase(fs_adapter, github_adapter)

        # Setup
        file_path = Path("inbox/doc.md")
        approved_dir = Path("approved")
        moved_path = approved_dir / "doc.md"

        doc_mock = Mock(spec=Document)
        doc_mock.content = "Test content"
        doc_mock.metadata = {"title": "Test Doc"}

        fs_adapter.read_document.return_value = doc_mock
        fs_adapter.safe_move_file.return_value = moved_path
        github_adapter.create_issue.side_effect = RuntimeError("GitHub API Error")

        # Execute & Verify
        with pytest.raises(RuntimeError, match="GitHub API Error"):
            usecase.process_single_file(file_path, approved_dir)

        # Verify Rollback
        # safe_move_file called twice: once for move, once for rollback
        assert fs_adapter.safe_move_file.call_count == 2

        # Check second call (rollback)
        rollback_call = fs_adapter.safe_move_file.call_args_list[1]
        assert rollback_call[0][0] == moved_path
        assert rollback_call[0][1] == file_path.parent
        assert rollback_call[1]["overwrite"] is True

    def test_process_all_files_success(self, mocks):
        """
        Given: inbox has files
        When: process_all_files is called
        Then: process_single_file logic is executed for each file
        """
        fs_adapter, github_adapter = mocks
        usecase = ApprovalUseCase(fs_adapter, github_adapter)

        inbox_dir = Path("inbox")
        approved_dir = Path("approved")

        # Use Mock objects instead of real Path objects
        file1 = Mock(spec=Path)
        file1.is_file.return_value = True
        file1.stem = "doc1"
        file1.parent = inbox_dir

        fs_adapter.list_files.return_value = [file1]

        doc_mock = Mock(spec=Document)
        doc_mock.content = "Content"
        doc_mock.metadata = {"title": "T"}
        fs_adapter.read_document.return_value = doc_mock
        fs_adapter.safe_move_file.return_value = approved_dir / "doc1.md"
        github_adapter.create_issue.return_value = 1

        result = usecase.process_all_files(inbox_dir, approved_dir)

        assert result is True
        fs_adapter.list_files.assert_called_once_with(inbox_dir)
        fs_adapter.read_document.assert_called()

    def test_process_all_files_empty(self, mocks):
        """
        Given: inbox has no files
        When: process_all_files is called
        Then: returns False
        """
        fs_adapter, github_adapter = mocks
        usecase = ApprovalUseCase(fs_adapter, github_adapter)

        fs_adapter.list_files.return_value = []

        result = usecase.process_all_files(Path("inbox"), Path("approved"))
        assert result is False

    def test_process_all_files_fail_fast(self, mocks):
        """
        Given: processing one file fails
        When: process_all_files is called
        Then: Exception is propagated immediately
        """
        fs_adapter, github_adapter = mocks
        usecase = ApprovalUseCase(fs_adapter, github_adapter)

        file1 = Mock(spec=Path)
        file1.is_file.return_value = True
        fs_adapter.list_files.return_value = [file1]

        # Make read_document fail
        fs_adapter.read_document.side_effect = RuntimeError("Read error")

        with pytest.raises(RuntimeError, match="Read error"):
            usecase.process_all_files(Path("inbox"), Path("approved"))
