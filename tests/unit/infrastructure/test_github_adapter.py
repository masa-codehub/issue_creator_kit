import os
from unittest.mock import MagicMock, patch

import pytest

from issue_creator_kit.domain.document import Document, Metadata
from issue_creator_kit.domain.exceptions import GitHubAPIError, GitHubRateLimitError
from issue_creator_kit.domain.interfaces import IGitHubAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter


class TestGitHubAdapter:
    @pytest.fixture
    def adapter(self):
        return GitHubAdapter(repo="test/repo", token="ghp_test")

    def test_protocol_conformance(self, adapter):
        assert isinstance(adapter, IGitHubAdapter)

    def test_init_raises_if_no_token(self):
        # Clear env to ensure no token
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError) as excinfo:
                GitHubAdapter(repo="test/repo", token="")
            assert "GitHub token is required" in str(excinfo.value)

            with pytest.raises(ValueError) as excinfo:
                GitHubAdapter(repo="test/repo", token=None)
            assert "GitHub token is required" in str(excinfo.value)

    def test_init_success_with_token(self):
        adapter = GitHubAdapter(repo="test/repo", token="ghp_test")
        assert adapter.token == "ghp_test"

    @patch("requests.post")
    def test_create_pull_request_success(self, mock_post, adapter):
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "html_url": "http://github.com/pr/1",
            "number": 1,
        }
        mock_post.return_value = mock_response

        # Execute
        url, number = adapter.create_pull_request("Title", "Body", "head", "main")

        # Verify
        assert url == "http://github.com/pr/1"
        assert number == 1
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_add_labels_success(self, mock_post, adapter):
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        # Execute
        adapter.add_labels(1, ["label1", "label2"])

        # Verify
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        assert "issues/1/labels" in args[0]
        assert kwargs["json"] == {"labels": ["label1", "label2"]}

    @patch("requests.post")
    def test_create_issue_api_error(self, mock_post, adapter):
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_post.return_value = mock_response

        # Execute & Verify
        with pytest.raises(GitHubAPIError) as excinfo:
            adapter.create_issue("Title", "Body")
        assert "500" in str(excinfo.value)
        assert "Internal Server Error" in str(excinfo.value)

    @patch("requests.post")
    def test_create_issue_rate_limit(self, mock_post, adapter):
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.headers = {"X-RateLimit-Remaining": "0"}
        mock_response.text = "Rate limit exceeded"
        mock_post.return_value = mock_response

        # Execute & Verify
        with pytest.raises(GitHubRateLimitError):
            adapter.create_issue("Title", "Body")

    @patch("requests.get")
    @patch("requests.post")
    def test_sync_issue_create_new(self, mock_post, mock_get, adapter):
        # Setup: No existing issue found via search
        mock_get_search = MagicMock()
        mock_get_search.status_code = 200
        mock_get_search.json.return_value = {"total_count": 0, "items": []}
        mock_get.return_value = mock_get_search

        mock_post_create = MagicMock()
        mock_post_create.status_code = 201
        mock_post_create.json.return_value = {"number": 123}
        mock_post.return_value = mock_post_create

        doc = Document(
            metadata=Metadata(
                id="task-001", title="Initial Task", phase="domain", status="Draft"
            ),
            content="Task body",
        )

        # Execute
        issue_id = adapter.sync_issue(doc)

        # Verify
        assert issue_id == 123
        mock_post.assert_called_once()
        kwargs = mock_post.call_args.kwargs
        assert "task-001: Initial Task" in kwargs["json"]["title"]
        assert "domain" in kwargs["json"]["labels"]

    @patch("requests.patch")
    def test_sync_issue_update_existing_by_id(self, mock_patch, adapter):
        # Setup: Metadata has issue_id
        mock_patch_res = MagicMock()
        mock_patch_res.status_code = 200
        mock_patch_res.json.return_value = {"number": 456}
        mock_patch.return_value = mock_patch_res

        doc = Document(
            metadata=Metadata(
                id="task-001", title="Task", issue_id=456, status="Issued"
            ),
            content="Updated content",
        )

        # Execute
        issue_id = adapter.sync_issue(doc)

        # Verify
        assert issue_id == 456
        mock_patch.assert_called_once()
        assert "issues/456" in mock_patch.call_args[0][0]

    @patch("requests.get")
    def test_find_or_create_issue_existing(self, mock_get, adapter):
        # Setup: Search returns one item
        mock_res = MagicMock()
        mock_res.status_code = 200
        mock_res.json.return_value = {
            "total_count": 1,
            "items": [{"number": 789, "title": "task-001: Task"}],
        }
        mock_get.return_value = mock_res

        # Execute
        issue_id = adapter.find_or_create_issue("task-001: Task", "Body")

        # Verify
        assert issue_id == 789
        mock_get.assert_called_once()
        assert "task-001: Task" in mock_get.call_args.kwargs["params"]["q"]
