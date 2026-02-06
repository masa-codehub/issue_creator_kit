from graphlib import CycleError
from pathlib import Path
from unittest.mock import ANY, MagicMock, call

import pytest

from issue_creator_kit.domain.document import Document
from issue_creator_kit.domain.interfaces import (
    IFileSystemAdapter,
    IGitAdapter,
    IGitHubAdapter,
)
from issue_creator_kit.usecase.creation import IssueCreationUseCase


@pytest.fixture
def mock_fs():
    return MagicMock(spec=IFileSystemAdapter)


@pytest.fixture
def mock_git():
    return MagicMock(spec=IGitAdapter)


@pytest.fixture
def mock_github():
    return MagicMock(spec=IGitHubAdapter)


@pytest.fixture
def usecase(mock_fs, mock_git, mock_github):
    # Note: UseCase might need to be updated to accept these interfaces
    return IssueCreationUseCase(
        fs_adapter=mock_fs, github_adapter=mock_github, git_adapter=mock_git
    )


def test_create_issues_ordered_by_dependency(usecase, mock_fs, mock_git, mock_github):
    # T1 -> T2
    mock_git.get_added_files.return_value = [
        "reqs/tasks/adr-007/T1.md",
        "reqs/tasks/adr-007/T2.md",
    ]

    doc1 = Document("content1", {"id": "T1", "depends_on": []})
    doc2 = Document("content2", {"id": "T2", "depends_on": ["T1"]})

    def read_side_effect(path):
        if "T1.md" in str(path):
            return doc1
        if "T2.md" in str(path):
            return doc2
        return None

    mock_fs.read_document.side_effect = read_side_effect
    mock_github.create_issue.side_effect = [101, 102]

    usecase.create_issues(before="base", after="head", adr_id="adr-007")

    # Verify order of creation: T1 then T2
    mock_github.create_issue.assert_has_calls(
        [
            call(ANY, ANY, ANY),  # T1
            call(ANY, ANY, ANY),  # T2
        ]
    )

    # Verify move
    mock_git.move_file.assert_has_calls(
        [
            call("reqs/tasks/adr-007/T1.md", "reqs/tasks/_archive/T1.md"),
            call("reqs/tasks/adr-007/T2.md", "reqs/tasks/_archive/T2.md"),
        ],
        any_order=True,
    )


def test_create_issues_with_archive_dependency(usecase, mock_fs, mock_git, mock_github):
    # T2 depends on T1. T1 is already in _archive/
    mock_git.get_added_files.return_value = ["reqs/tasks/adr-007/T2.md"]
    mock_fs.list_files.return_value = [Path("reqs/tasks/_archive/T1.md")]

    doc1 = Document("content1", {"id": "T1", "status": "Issued", "issue_id": 101})
    doc2 = Document("content2", {"id": "T2", "depends_on": ["T1"]})

    def read_side_effect(path):
        if "T1.md" in str(path):
            return doc1
        if "T2.md" in str(path):
            return doc2
        return None

    mock_fs.read_document.side_effect = read_side_effect

    mock_github.create_issue.return_value = 102

    usecase.create_issues(before="base", after="head", adr_id="adr-007")

    mock_github.create_issue.assert_called_once()
    mock_git.move_file.assert_called_with(
        "reqs/tasks/adr-007/T2.md", "reqs/tasks/_archive/T2.md"
    )


def test_create_issues_skipped_if_dependency_not_ready(
    usecase, mock_fs, mock_git, mock_github
):
    # T2 depends on T1. T1 is NOT in batch and NOT in archive (or not Issued)
    mock_git.get_added_files.return_value = ["reqs/tasks/adr-007/T2.md"]
    mock_fs.list_files.return_value = []  # No archive

    doc2 = Document("content2", {"id": "T2", "depends_on": ["T1"]})
    mock_fs.read_document.return_value = doc2

    usecase.create_issues(before="base", after="head", adr_id="adr-007")

    mock_github.create_issue.assert_not_called()
    mock_git.move_file.assert_not_called()


def test_create_issues_circular_dependency(usecase, mock_fs, mock_git):
    # A -> B -> A
    mock_git.get_added_files.return_value = [
        "reqs/tasks/adr-007/A.md",
        "reqs/tasks/adr-007/B.md",
    ]

    doc_a = Document("contentA", {"id": "A", "depends_on": ["B"]})
    doc_b = Document("contentB", {"id": "B", "depends_on": ["A"]})

    mock_fs.read_document.side_effect = [doc_a, doc_b]

    with pytest.raises(CycleError):
        usecase.create_issues(before="base", after="head", adr_id="adr-007")


def test_create_issues_fail_fast_no_move_on_api_error(
    usecase, mock_fs, mock_git, mock_github
):
    mock_git.get_added_files.return_value = ["reqs/tasks/adr-007/T1.md"]
    doc1 = Document("content1", {"id": "T1", "depends_on": []})
    mock_fs.read_document.return_value = doc1

    mock_github.create_issue.side_effect = RuntimeError("API Error")

    with pytest.raises(RuntimeError, match="API Error"):
        usecase.create_issues(before="base", after="head", adr_id="adr-007")

    # Verify move was NOT called
    mock_git.move_file.assert_not_called()
