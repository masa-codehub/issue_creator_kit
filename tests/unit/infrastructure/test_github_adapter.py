import os
import unittest
from unittest.mock import patch

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
