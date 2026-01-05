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
def usecase(mock_fs, mock_github, mock_git):
    return IssueCreationUseCase(mock_fs, mock_github, mock_git)


def test_create_issues_from_virtual_queue_success(
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
    mock_github.create_issue.side_effect = [101, 102]

    # Execute
    usecase.create_issues_from_virtual_queue(
        base_ref="before", head_ref="after", archive_path="reqs/tasks/archive/"
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

    # Verify git operations
    mock_git.add.assert_called()
    mock_git.commit.assert_called_with("docs: update issue numbers")


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
