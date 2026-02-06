from unittest.mock import MagicMock

import pytest

from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter
from issue_creator_kit.infrastructure.git_adapter import GitAdapter
from issue_creator_kit.infrastructure.github_adapter import GitHubAdapter
from issue_creator_kit.usecase.creation import IssueCreationUseCase
from issue_creator_kit.usecase.roadmap_sync import RoadmapSyncUseCase


class TestIssueCreationIntegration:
    @pytest.fixture
    def setup_env(self, tmp_path):
        # Setup directory structure
        tasks_dir = tmp_path / "reqs" / "tasks" / "adr-007"
        archive_dir = tmp_path / "reqs" / "tasks" / "archive"
        tasks_dir.mkdir(parents=True)
        archive_dir.mkdir(parents=True)

        # Create a roadmap file
        roadmap_path = tmp_path / "roadmap.md"
        roadmap_path.write_text("""## Roadmap
| Task | Link |
| --- | --- |
| t1 | [t1.md](reqs/tasks/drafts/adr-007/t1.md) |
""")

        # Create a task file
        task_file = tasks_dir / "t1.md"
        task_file.write_text("""---
id: t1
status: Ready
title: Task 1
---
Body of t1""")

        return {
            "root": tmp_path,
            "tasks_dir": tasks_dir,
            "archive_dir": archive_dir,
            "roadmap_path": roadmap_path,
            "task_file": task_file,
        }

    def test_full_creation_flow(self, setup_env, monkeypatch):
        root = setup_env["root"]
        monkeypatch.chdir(root)

        # Adapters
        fs = FileSystemAdapter()
        mock_git = MagicMock(spec=GitAdapter)
        mock_github = MagicMock(spec=GitHubAdapter)
        roadmap_sync = RoadmapSyncUseCase(fs)

        usecase = IssueCreationUseCase(
            fs_adapter=fs,
            github_adapter=mock_github,
            git_adapter=mock_git,
            roadmap_sync=roadmap_sync,
        )

        # Mock Git behavior
        mock_git.get_added_files.return_value = ["reqs/tasks/adr-007/t1.md"]
        mock_git.get_current_branch.return_value = "main"

        # Mock GitHub behavior
        mock_github.create_issue.return_value = 123

        # Execute
        usecase.create_issues(
            before="base", after="head", adr_id="adr-007", roadmap_path="roadmap.md"
        )

        # 1. Verify File Movement (git mv should be called)
        mock_git.move_file.assert_called_once_with(
            "reqs/tasks/adr-007/t1.md", "reqs/tasks/archive/t1.md"
        )

        # 2. Verify File Metadata Update (in the archive)
        # Note: In reality, fs.save_document happens BEFORE git mv in the code,
        # but since we are using real filesystem and mock git, the file on disk
        # will have been updated at the original path.
        # Since git.move_file is mocked, the file isn't actually moved.
        # But fs.save_document was called on the original path.
        original_file = setup_env["tasks_dir"] / "t1.md"
        updated_doc = fs.read_document(original_file)
        assert updated_doc.metadata["status"] == "Issued"
        assert updated_doc.metadata["issue_id"] == 123

        # 3. Verify Roadmap Sync
        roadmap_content = setup_env["roadmap_path"].read_text()
        assert "reqs/tasks/archive/adr-007/t1.md" in roadmap_content
        assert "(#123)" in roadmap_content

        # 4. Verify Git Commit & Push
        mock_git.add.assert_called()
        # Should add archived file and roadmap
        all_added = []
        for call_args in mock_git.add.call_args_list:
            all_added.extend(call_args[0][0])
        assert "reqs/tasks/archive/t1.md" in all_added
        assert "roadmap.md" in all_added

        mock_git.commit.assert_called_with(
            "docs: update issue numbers and sync roadmap"
        )
        mock_git.push.assert_called_with(remote="origin", branch="main")
