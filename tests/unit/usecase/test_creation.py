from pathlib import Path
from unittest.mock import MagicMock

import pytest

from issue_creator_kit.domain.document import Document
from issue_creator_kit.usecase.creation import IssueCreationUseCase


@pytest.fixture
def mock_fs():
    return MagicMock()


@pytest.fixture
def mock_github():
    return MagicMock()


@pytest.fixture
def mock_git():
    return MagicMock()


@pytest.fixture
def mock_roadmap_sync():
    return MagicMock()


@pytest.fixture
def usecase(mock_fs, mock_github, mock_git, mock_roadmap_sync):
    return IssueCreationUseCase(mock_fs, mock_github, mock_git, mock_roadmap_sync)


def test_create_issues_from_virtual_queue_success(
    usecase, mock_fs, mock_github, mock_git, mock_roadmap_sync, tmp_path
):
    # Setup
    mock_git.get_added_files.return_value = [
        "reqs/tasks/archive/phase-1/issue-T1-1.md",
        "reqs/tasks/archive/phase-1/issue-T1-2.md",
    ]

    doc1 = Document(content="Body 1", metadata={"title": "Task 1"})
    doc2 = Document(content="Body 2", metadata={"title": "Task 2"})

    mock_fs.read_document.side_effect = [doc1, doc2]
    mock_github.create_issue.side_effect = [101, 102]

    # Create physical roadmap file for exists() check
    roadmap_file = tmp_path / "roadmap.md"
    roadmap_file.touch()

    # Execute
    usecase.create_issues_from_virtual_queue(
        base_ref="before",
        head_ref="after",
        archive_path="reqs/tasks/archive/",
        roadmap_path=str(roadmap_file),
    )

    # Verify
    assert mock_github.create_issue.call_count == 2

    # Verify metadata updates (Atomic write-back)
    assert mock_fs.update_metadata.call_count == 2
    mock_fs.update_metadata.assert_any_call(
        Path("reqs/tasks/archive/phase-1/issue-T1-1.md"), {"issue": "#101"}
    )
    mock_fs.update_metadata.assert_any_call(
        Path("reqs/tasks/archive/phase-1/issue-T1-2.md"), {"issue": "#102"}
    )

    # Verify roadmap sync call with correct arguments
    expected_results = [
        (Path("reqs/tasks/archive/phase-1/issue-T1-1.md"), 101),
        (Path("reqs/tasks/archive/phase-1/issue-T1-2.md"), 102),
    ]
    mock_roadmap_sync.sync.assert_called_once_with(str(roadmap_file), expected_results)

    # Verify git operations
    mock_git.add.assert_called()
    # Check that roadmap was added
    add_args = mock_git.add.call_args[0][0]
    assert str(roadmap_file) in add_args
    mock_git.commit.assert_called_with("docs: update issue numbers and sync roadmap")


def test_create_issues_from_virtual_queue_roadmap_sync_failure(
    usecase, mock_fs, mock_github, mock_git, mock_roadmap_sync, tmp_path
):
    # Setup
    mock_git.get_added_files.return_value = ["reqs/tasks/archive/task1.md"]
    mock_fs.read_document.return_value = Document(
        content="Body", metadata={"title": "Task 1"}
    )
    mock_github.create_issue.return_value = 101

    # Create physical roadmap file for exists() check
    roadmap_file = tmp_path / "roadmap.md"
    roadmap_file.touch()

    # Simulate Roadmap sync failure
    mock_roadmap_sync.sync.side_effect = ValueError("Sync Error")

    # Execute
    usecase.create_issues_from_virtual_queue(
        base_ref="before",
        head_ref="after",
        archive_path="reqs/tasks/archive/",
        roadmap_path=str(roadmap_file),
    )

    # Verify: Process should continue (metadata updated) but roadmap not added to git
    assert mock_fs.update_metadata.call_count == 1
    mock_git.add.assert_called_once_with(["reqs/tasks/archive/task1.md"])
    mock_git.commit.assert_called()


def test_create_issues_from_virtual_queue_fail_fast(
    usecase, mock_fs, mock_github, mock_git
):
    # Setup
    mock_git.get_added_files.return_value = [
        "reqs/tasks/archive/phase-1/issue-T1-1.md",
        "reqs/tasks/archive/phase-1/issue-T1-2.md",
    ]

    doc1 = Document(content="Body 1", metadata={"title": "Task 1"})
    doc2 = Document(content="Body 2", metadata={"title": "Task 2"})

    mock_fs.read_document.side_effect = [doc1, doc2]
    # Fail on second issue
    mock_github.create_issue.side_effect = [101, RuntimeError("API Error")]

    # Execute & Verify Exception
    with pytest.raises(RuntimeError, match="API Error"):
        usecase.create_issues_from_virtual_queue(
            base_ref="before", head_ref="after", archive_path="reqs/tasks/archive/"
        )

    # Verify Fail-fast: No metadata updates should happen if any fail
    mock_fs.update_metadata.assert_not_called()
    mock_git.commit.assert_not_called()


def test_create_issues_from_virtual_queue_skips_processed(
    usecase, mock_fs, mock_github, mock_git
):
    # Setup
    mock_git.get_added_files.return_value = [
        "reqs/tasks/archive/phase-1/issue-T1-1.md",
        "reqs/tasks/archive/phase-1/issue-T1-2.md",
    ]

    # doc1 already has issue number
    doc1 = Document(content="Body 1", metadata={"title": "Task 1", "issue": "#100"})
    doc2 = Document(content="Body 2", metadata={"title": "Task 2"})

    mock_fs.read_document.side_effect = [doc1, doc2]
    mock_github.create_issue.return_value = 102

    # Execute
    usecase.create_issues_from_virtual_queue(
        base_ref="before", head_ref="after", archive_path="reqs/tasks/archive/"
    )

    # Verify only doc2 was processed
    assert mock_github.create_issue.call_count == 1
    mock_github.create_issue.assert_called_with("Task 2", "Body 2", [])
    mock_fs.update_metadata.assert_called_once_with(
        Path("reqs/tasks/archive/phase-1/issue-T1-2.md"), {"issue": "#102"}
    )


def test_create_issues_from_virtual_queue_with_dependencies(
    usecase, mock_fs, mock_github, mock_git
):
    # Setup
    mock_git.get_added_files.return_value = [
        "reqs/tasks/archive/task1.md",
        "reqs/tasks/archive/task2.md",
    ]

    # task2 depends on task1
    doc1 = Document(content="Body 1", metadata={"title": "Task 1"})
    doc2 = Document(
        content="Body 2 depends on task1.md",
        metadata={"title": "Task 2", "depends_on": ["task1.md"]},
    )

    # Mock read_document to return based on path
    def side_effect(path):
        if "task1.md" in str(path):
            return doc1
        return doc2

    mock_fs.read_document.side_effect = side_effect
    mock_github.create_issue.side_effect = [101, 102]

    # Execute
    usecase.create_issues_from_virtual_queue(
        base_ref="before", head_ref="after", archive_path="reqs/tasks/archive/"
    )

    # Verify order: Task 1 should be created before Task 2
    assert mock_github.create_issue.call_count == 2

    # Check calls
    calls = mock_github.create_issue.call_args_list
    assert calls[0].args[0] == "Task 1"
    assert calls[1].args[0] == "Task 2"
    # Verify body replacement in Task 2
    assert "#101" in calls[1].args[1]
    assert "task1.md" not in calls[1].args[1]


def test_create_issues_from_virtual_queue_with_metadata_pr(
    usecase, mock_fs, mock_github, mock_git
):
    # Setup
    mock_git.get_added_files.return_value = ["reqs/tasks/archive/task1.md"]
    mock_fs.read_document.return_value = Document(
        content="Body", metadata={"title": "Task 1"}
    )
    mock_github.create_issue.return_value = 101

    # Execute with use_pr=True
    usecase.create_issues_from_virtual_queue(
        base_ref="before",
        head_ref="after",
        archive_path="reqs/tasks/archive/",
        use_pr=True,
    )

    # Verify branch creation and PR
    mock_git.checkout.assert_called()
    # Find the branch name used
    checkout_args = mock_git.checkout.call_args[0][0]
    assert "chore/metadata-sync-" in checkout_args

    mock_git.push.assert_called_with(remote="origin", branch=checkout_args)
    mock_github.create_pull_request.assert_called_once()
    pr_args = mock_github.create_pull_request.call_args[1]
    assert pr_args["head"] == checkout_args
    assert pr_args["base"] == "main"
