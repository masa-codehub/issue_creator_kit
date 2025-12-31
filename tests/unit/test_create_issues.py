import os
from unittest.mock import MagicMock, patch

import pytest


@pytest.fixture
def mock_utils():
    with patch("issue_creator_kit.scripts.create_issues.utils") as mock:
        yield mock


def test_get_dependencies_yaml(tmp_path, mock_utils):
    # 環境変数をモック化してインポート (sys.exit を避けるため)
    with patch.dict(
        os.environ, {"GITHUB_REPOSITORY": "owner/repo", "GH_TOKEN": "token"}
    ):
        from issue_creator_kit.scripts import create_issues

        file1 = tmp_path / "issue-1.md"
        file2 = tmp_path / "issue-2.md"
        file1.touch()
        file2.touch()

        # utils.load_document の戻り値を設定
        mock_utils.load_document.side_effect = [
            ({"title": "Issue 1", "depends_on": ["issue-2.md"]}, "# Body 1"),
            ({"title": "Issue 2", "depends_on": []}, "# Body 2"),
        ]

        files = [str(file1), str(file2)]
        graph, file_map = create_issues.get_dependencies(files)

        assert "issue-1.md" in graph
        assert "issue-2.md" in graph
        assert "issue-2.md" in graph["issue-1.md"]
        assert len(graph["issue-2.md"]) == 0


def test_get_dependencies_legacy_formats(tmp_path, mock_utils):
    with patch.dict(
        os.environ, {"GITHUB_REPOSITORY": "owner/repo", "GH_TOKEN": "token"}
    ):
        from issue_creator_kit.scripts import create_issues

        file1 = tmp_path / "legacy.md"
        file1.touch()

        # カンマ区切り文字列と (none) の混在
        mock_utils.load_document.return_value = (
            {"Depends-On": "dep1.md, dep2.md, (none)"},
            "",
        )

        graph, _ = create_issues.get_dependencies([str(file1)])
        deps = graph["legacy.md"]
        assert "dep1.md" in deps
        assert "dep2.md" in deps
        assert "(none)" not in deps


def test_create_issue_replace_links(tmp_path, mock_utils):
    with patch.dict(
        os.environ, {"GITHUB_REPOSITORY": "owner/repo", "GH_TOKEN": "token"}
    ):
        from issue_creator_kit.scripts import create_issues

        file_path = tmp_path / "issue-1.md"
        file_path.touch()

        with patch("issue_creator_kit.scripts.create_issues.requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"number": 101}
            mock_requests.post.return_value = mock_response

            issue_map = {"issue-2.md": 202}
            mock_utils.load_document.return_value = (
                {"title": "Issue 1"},
                "Depends on issue-2.md",
            )

            create_issues.create_issue(
                "issue-1.md", str(file_path), issue_map, "owner/repo", "token"
            )

            # ペイロードの確認
            call_args = mock_requests.post.call_args[1]
            data = call_args["json"]
            assert "Depends on #202" in data["body"]


def test_create_issue_labels(tmp_path, mock_utils):
    with patch.dict(
        os.environ, {"GITHUB_REPOSITORY": "owner/repo", "GH_TOKEN": "token"}
    ):
        from issue_creator_kit.scripts import create_issues

        file_path = tmp_path / "test.md"
        file_path.touch()

        with patch("issue_creator_kit.scripts.create_issues.requests") as mock_requests:
            mock_response = MagicMock()
            mock_response.status_code = 201
            mock_response.json.return_value = {"number": 1}
            mock_requests.post.return_value = mock_response

            # Case 1: リスト形式のラベル
            mock_utils.load_document.return_value = ({"labels": ["bug", "high"]}, "")
            create_issues.create_issue(
                "test.md", str(file_path), {}, "owner/repo", "token"
            )
            assert mock_requests.post.call_args[1]["json"]["labels"] == ["bug", "high"]

            # Case 2: 文字列形式のラベル（カンマ区切り）
            mock_utils.load_document.return_value = (
                {"labels": "task, documentation, "},
                "",
            )
            create_issues.create_issue(
                "test.md", str(file_path), {}, "owner/repo", "token"
            )
            assert mock_requests.post.call_args[1]["json"]["labels"] == [
                "task",
                "documentation",
            ]
