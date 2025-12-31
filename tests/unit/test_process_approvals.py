import os
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from github import GithubException

from issue_creator_kit.scripts import process_approvals


@pytest.fixture
def mock_utils():
    with patch("issue_creator_kit.scripts.process_approvals.utils") as mock:
        yield mock


@pytest.fixture
def mock_github():
    with patch("issue_creator_kit.scripts.process_approvals.Github") as mock:
        yield mock


def test_process_approval_success(mock_utils, mock_github):
    # Setup
    file_path = Path("reqs/design/_inbox/test.md")
    approved_dir = Path("reqs/design/_approved")

    # Mock load_document
    mock_utils.load_document.return_value = (
        {"title": "Test Doc", "Status": "提案中"},
        "# Content",
    )

    # Mock move
    moved_path = approved_dir / "test.md"
    mock_utils.safe_move_file.return_value = moved_path

    # Mock GitHub
    mock_repo = MagicMock()
    mock_issue = MagicMock()
    mock_issue.number = 123
    mock_repo.create_issue.return_value = mock_issue
    mock_github.return_value.get_repo.return_value = mock_repo

    # Execute
    process_approvals.process_single_file(
        file_path, approved_dir, repo_name="owner/repo", token="token"
    )

    # Verify
    # 1. Update Status
    first_call_args = mock_utils.update_metadata.call_args_list[0]
    args, _ = first_call_args
    assert args[0] == file_path
    assert args[1]["Status"] == "承認済み"
    assert "Date" in args[1]

    # 2. Move File
    mock_utils.safe_move_file.assert_called_with(file_path, approved_dir)

    # 3. Create Issue
    mock_repo.create_issue.assert_called_once()
    call_args = mock_repo.create_issue.call_args[1]
    assert call_args["title"] == "Test Doc"
    assert "reqs/design/_approved/test.md" in call_args["body"]

    # 4. Update Issue Number in Moved File
    # 2回目の update_metadata 呼び出しを確認 (process_single_file内のステップ5)
    last_call_args = mock_utils.update_metadata.call_args_list[-1]
    args, _ = last_call_args
    assert args[0] == moved_path
    assert args[1]["Issue"] == "#123"


def test_process_approval_file_not_found(mock_utils):
    file_path = Path("non_existent.md")
    mock_utils.load_document.side_effect = FileNotFoundError

    with pytest.raises(FileNotFoundError):
        process_approvals.process_single_file(
            file_path, Path("dst"), "owner/repo", "token"
        )


def test_process_approval_rollback_on_github_error(mock_utils, mock_github):
    # Setup
    file_path = Path("reqs/design/_inbox/test.md")
    approved_dir = Path("reqs/design/_approved")
    moved_path = approved_dir / "test.md"

    mock_utils.load_document.return_value = ({"title": "T"}, "C")
    mock_utils.safe_move_file.return_value = moved_path

    # GitHub Error
    mock_github.return_value.get_repo.side_effect = Exception("GitHub is down")

    # Execute & Verify
    with pytest.raises(Exception) as exc:
        process_approvals.process_single_file(
            file_path, approved_dir, "owner/repo", "token"
        )
    assert "GitHub is down" in str(exc.value)

    # Verify rollback: moved_path から file_path.parent へ戻されていること
    mock_utils.safe_move_file.assert_any_call(
        moved_path, file_path.parent, overwrite=True
    )


def test_process_approval_summary_logic(mock_utils, mock_github):
    # Setup
    file_path = Path("test.md")
    content_long = "A" * 300
    content_short = "A" * 10

    mock_utils.load_document.return_value = ({"title": "T"}, content_long)
    mock_utils.safe_move_file.return_value = Path("moved.md")

    mock_repo = MagicMock()
    mock_github.return_value.get_repo.return_value = mock_repo

    # Case 1: Long content (should have ...)
    process_approvals.process_single_file(file_path, Path("dst"), "o/r", "t")
    issue_body = mock_repo.create_issue.call_args[1]["body"]
    assert "A" * 200 + "..." in issue_body

    # Case 2: Short content (should NOT have ...)
    mock_utils.load_document.return_value = ({"title": "T"}, content_short)
    process_approvals.process_single_file(file_path, Path("dst"), "o/r", "t")
    issue_body = mock_repo.create_issue.call_args[1]["body"]
    assert "A" * 10 in issue_body
    assert "A" * 10 + "..." not in issue_body


def test_process_approval_last_updated_key(mock_utils, mock_github):
    # Setup
    file_path = Path("test.md")
    mock_utils.load_document.return_value = ({"Last Updated": "old"}, "C")
    mock_utils.safe_move_file.return_value = Path("moved.md")

    mock_repo = MagicMock()
    mock_github.return_value.get_repo.return_value = mock_repo

    # Execute
    process_approvals.process_single_file(file_path, Path("dst"), "o/r", "t")

    # Verify: "Last Updated" key is updated
    first_update_args = mock_utils.update_metadata.call_args_list[0][0]
    assert "Last Updated" in first_update_args[1]
    assert first_update_args[1]["Last Updated"] == datetime.now().strftime("%Y-%m-%d")


def test_main_missing_token(capsys):
    # 環境変数を空にしてトークン欠如エラーを確認
    with (
        patch.dict(os.environ, {}, clear=True),
        patch("sys.argv", ["script.py", "test.md", "--repo", "o/r"]),
        pytest.raises(SystemExit) as exc,
    ):
        process_approvals.main()
    assert exc.value.code == 1
    captured = capsys.readouterr()
    assert "GitHub Token is required" in captured.err


def test_main_github_exception(capsys, mock_github, mock_utils):
    # GithubException 発生時のエラー出力を確認
    with (
        patch.dict(os.environ, {"GITHUB_TOKEN": "token"}),
        patch("sys.argv", ["script.py", "test.md", "--repo", "o/r"]),
    ):
        mock_utils.load_document.return_value = ({"title": "T"}, "C")
        mock_utils.safe_move_file.return_value = Path("moved.md")
        # GithubException をシミュレート
        mock_github.return_value.get_repo.side_effect = GithubException(
            404, {"message": "Not Found"}
        )

        with pytest.raises(SystemExit) as exc:
            process_approvals.main()
        assert exc.value.code == 1
        captured = capsys.readouterr()
        assert "GitHub API Error" in captured.err
