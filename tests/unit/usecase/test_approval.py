from unittest.mock import ANY, MagicMock

import pytest

from issue_creator_kit.domain.document import Document, Metadata
from issue_creator_kit.usecase.approval import ApprovalUseCase


class TestApprovalUseCase:
    @pytest.fixture
    def mock_fs(self):
        return MagicMock()

    @pytest.fixture
    def mock_github(self):
        return MagicMock()

    @pytest.fixture
    def usecase(self, mock_fs, mock_github):
        return ApprovalUseCase(mock_fs, mock_github)

    def test_process_single_file_success(self, usecase, mock_fs, mock_github, tmp_path):
        # Setup
        file_path = tmp_path / "inbox/test.md"
        approved_dir = tmp_path / "approved"

        metadata = Metadata(id="test-doc", status="Draft", title="Test Title")
        doc = Document(content="Body content", metadata=metadata)
        mock_fs.read_document.return_value = doc
        mock_fs.safe_move_file.return_value = approved_dir / "test.md"
        mock_github.create_issue.return_value = 123

        # Execute
        usecase.process_single_file(file_path, approved_dir)

        # Verify
        mock_fs.read_document.assert_called_once_with(file_path)
        # Verify metadata update (Status and Date)
        mock_fs.update_metadata.assert_any_call(
            file_path, {"status": "Approved", "date": ANY}
        )
        mock_fs.update_metadata.assert_any_call(
            approved_dir / "test.md", {"issue_id": 123}
        )
        mock_github.create_issue.assert_called_once()
        assert mock_github.create_issue.call_args[1]["title"] == "Test Title"

    def test_process_single_file_rollback(
        self, usecase, mock_fs, mock_github, tmp_path
    ):
        # Setup
        file_path = tmp_path / "inbox/test.md"
        approved_dir = tmp_path / "approved"

        metadata = Metadata(id="test-doc", status="Draft")
        doc = Document(content="Body", metadata=metadata)
        mock_fs.read_document.return_value = doc
        moved_path = approved_dir / "test.md"
        mock_fs.safe_move_file.return_value = moved_path

        # Simulate GitHub failure
        mock_github.create_issue.side_effect = RuntimeError("GitHub Down")

        # Execute & Verify Exception
        with pytest.raises(RuntimeError, match="GitHub Down"):
            usecase.process_single_file(file_path, approved_dir)

        # Verify Rollback: moved file is moved back
        mock_fs.safe_move_file.assert_any_call(
            moved_path, file_path.parent, overwrite=True
        )
