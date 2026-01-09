import subprocess
import unittest
from unittest.mock import patch

from issue_creator_kit.infrastructure.git_adapter import GitAdapter


class TestGitAdapter(unittest.TestCase):
    def setUp(self):
        self.adapter = GitAdapter()

    @patch("subprocess.run")
    def test_run_command_sanitizes_error(self, mock_run):
        # Given
        # 300 chars > 200 chars limit
        long_secret = "A" * 300
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd=["git", "push"], output="output", stderr=long_secret
        )

        # When/Then
        with self.assertRaises(RuntimeError) as cm:
            self.adapter.run_command(["push"])

        # Verify
        msg = str(cm.exception)
        self.assertIn("Git command failed: AAAAA", msg)
        # Check it ends with ...
        self.assertTrue(msg.endswith("..."))
        # Check length (prefix + 200)
        # Prefix "Git command failed: " is 20 chars.
        # Total around 220.
        self.assertTrue(len(msg) < 250)

    @patch("subprocess.run")
    def test_fetch_success(self, mock_run):
        # When
        self.adapter.fetch(remote="origin", prune=True)

        # Then
        mock_run.assert_called_with(
            ["git", "fetch", "origin", "--prune"],
            check=True,
            capture_output=True,
            text=True,
        )

    @patch("subprocess.run")
    def test_fetch_failure(self, mock_run):
        # Given
        mock_run.side_effect = subprocess.CalledProcessError(
            returncode=1, cmd="git fetch", stderr="Network error"
        )

        # When/Then
        with self.assertRaises(RuntimeError) as cm:
            self.adapter.fetch()

        self.assertIn("Network error", str(cm.exception))
