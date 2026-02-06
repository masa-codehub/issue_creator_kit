from graphlib import CycleError
from pathlib import Path
from unittest.mock import MagicMock, call

import pytest

from issue_creator_kit.domain.document import Document, Metadata
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
    return IssueCreationUseCase(
        fs_adapter=mock_fs, github_adapter=mock_github, git_adapter=mock_git
    )


def test_create_issues_ordered_by_dependency(usecase, mock_fs, mock_git, mock_github):
    # T1 -> T2
    mock_git.get_added_files.return_value = [
        "reqs/tasks/adr-007/t1.md",
        "reqs/tasks/adr-007/t2.md",
    ]

    doc1 = Document("content1", Metadata(id="t1", status="Ready"))
    doc2 = Document("content2", Metadata(id="t2", status="Ready", depends_on=["t1"]))

    def read_side_effect(path):
        if "t1.md" in str(path):
            return doc1
        if "t2.md" in str(path):
            return doc2
        return None

    mock_fs.read_document.side_effect = read_side_effect
    mock_github.create_issue.side_effect = [101, 102]
    mock_git.get_current_branch.return_value = "main"

    usecase.create_issues(before="base", after="head", adr_id="adr-007")

    # Verify order of creation: t1 then t2
    calls = mock_github.create_issue.call_args_list
    assert len(calls) == 2
    # 1st call for t1
    assert "t1" in calls[0].args[0] or (
        calls[0].kwargs.get("title") and "t1" in calls[0].kwargs["title"]
    )
    # 2nd call for t2
    assert "t2" in calls[1].args[0] or (
        calls[1].kwargs.get("title") and "t2" in calls[1].kwargs["title"]
    )

    # Verify move
    mock_git.move_file.assert_has_calls(
        [
            call("reqs/tasks/adr-007/t1.md", "reqs/tasks/archive/t1.md"),
            call("reqs/tasks/adr-007/t2.md", "reqs/tasks/archive/t2.md"),
        ],
        any_order=True,
    )

    # Verify commit
    mock_git.commit.assert_called_with("docs: update issue numbers and sync roadmap")


def test_create_issues_with_roadmap_sync(usecase, mock_fs, mock_git, mock_github):
    mock_git.get_added_files.return_value = ["reqs/tasks/adr-007/t1.md"]
    doc1 = Document("content1", Metadata(id="t1", status="Ready"))
    mock_fs.read_document.return_value = doc1
    mock_github.create_issue.return_value = 101
    mock_git.get_current_branch.return_value = "main"

    # UseCase should have roadmap_sync mocked via fixture
    usecase.roadmap_sync = MagicMock()

    usecase.create_issues(
        before="base", after="head", adr_id="adr-007", roadmap_path="roadmap.md"
    )

    usecase.roadmap_sync.sync.assert_called_once()
    # Check if roadmap.md was added to git
    mock_git.add.assert_called()
    added_files = mock_git.add.call_args[0][0]
    assert "roadmap.md" in added_files


def test_create_issues_with_archive_dependency(usecase, mock_fs, mock_git, mock_github):
    # t2 depends on t1. t1 is already in archive/
    mock_git.get_added_files.return_value = ["reqs/tasks/adr-007/t2.md"]
    mock_fs.list_files.return_value = [Path("reqs/tasks/archive/t1.md")]

    doc1 = Document(
        "content1",
        Metadata(id="t1", status="Issued", issue_id=101, parent="p1", phase="1"),
    )
    doc2 = Document("content2", Metadata(id="t2", status="Ready", depends_on=["t1"]))

    def read_side_effect(path):
        if "t1.md" in str(path):
            return doc1
        if "t2.md" in str(path):
            return doc2
        return None

    mock_fs.read_document.side_effect = read_side_effect
    mock_github.create_issue.return_value = 102
    mock_git.get_current_branch.return_value = "main"

    usecase.create_issues(before="base", after="head", adr_id="adr-007")

    mock_github.create_issue.assert_called_once()
    mock_git.move_file.assert_called_with(
        "reqs/tasks/adr-007/t2.md", "reqs/tasks/archive/t2.md"
    )


def test_create_issues_skipped_if_dependency_not_ready(
    usecase, mock_fs, mock_git, mock_github
):
    # t2 depends on t1. t1 is NOT in batch and NOT in archive (or not Issued)
    mock_git.get_added_files.return_value = ["reqs/tasks/adr-007/t2.md"]
    mock_fs.list_files.return_value = []  # No archive

    doc2 = Document("content2", Metadata(id="t2", status="Ready", depends_on=["t1"]))
    mock_fs.read_document.return_value = doc2

    with pytest.raises(RuntimeError, match="Missing dependency: t1"):
        usecase.create_issues(before="base", after="head", adr_id="adr-007")

    mock_github.create_issue.assert_not_called()
    mock_git.move_file.assert_not_called()


def test_create_issues_circular_dependency(usecase, mock_fs, mock_git):
    # a -> b -> a
    mock_git.get_added_files.return_value = [
        "reqs/tasks/adr-007/a.md",
        "reqs/tasks/adr-007/b.md",
    ]

    doc_a = Document("contentA", Metadata(id="a", status="Ready", depends_on=["b"]))
    doc_b = Document("contentB", Metadata(id="b", status="Ready", depends_on=["a"]))

    mock_fs.read_document.side_effect = [doc_a, doc_b]

    with pytest.raises(CycleError):
        usecase.create_issues(before="base", after="head", adr_id="adr-007")


def test_create_issues_fail_fast_no_move_on_api_error(
    usecase, mock_fs, mock_git, mock_github
):
    mock_git.get_added_files.return_value = ["reqs/tasks/adr-007/t1.md"]
    doc1 = Document("content1", Metadata(id="t1", status="Ready"))
    mock_fs.read_document.return_value = doc1

    mock_github.create_issue.side_effect = RuntimeError("API Error")

    with pytest.raises(RuntimeError, match="API Error"):
        usecase.create_issues(before="base", after="head", adr_id="adr-007")

    # Verify move was NOT called
    mock_git.move_file.assert_not_called()
