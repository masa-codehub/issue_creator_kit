import os
import unittest
from unittest.mock import MagicMock, patch

from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter


class TestGitHubAdapter(unittest.TestCase):
    def test_init_raises_if_no_token(self):
        # Clear env to ensure no token
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError) as cm:
                GitHubAdapter(repo="test/repo", token="")
            self.assertIn("GitHub token is required", str(cm.exception))

            with self.assertRaises(ValueError) as cm:
                GitHubAdapter(repo="test/repo", token=None)
            self.assertIn("GitHub token is required", str(cm.exception))

    def test_init_success_with_token(self):
        adapter = GitHubAdapter(repo="test/repo", token="ghp_test")
        self.assertEqual(adapter.token, "ghp_test")

    @patch("requests.post")
    def test_create_pull_request_success(self, mock_post):
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {
            "html_url": "http://github.com/pr/1",
            "number": 1,
        }
        mock_post.return_value = mock_response
        adapter = GitHubAdapter(repo="test/repo", token="ghp_test")

        # Execute
        url, number = adapter.create_pull_request("Title", "Body", "head", "main")

        # Verify
        self.assertEqual(url, "http://github.com/pr/1")
        self.assertEqual(number, 1)
        mock_post.assert_called_once()

    @patch("requests.post")
    def test_add_labels_success(self, mock_post):
        # Setup
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response
        adapter = GitHubAdapter(repo="test/repo", token="ghp_test")

        # Execute
        adapter.add_labels(1, ["label1", "label2"])

        # Verify
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn("issues/1/labels", args[0])
        self.assertEqual(kwargs["json"], {"labels": ["label1", "label2"]})
