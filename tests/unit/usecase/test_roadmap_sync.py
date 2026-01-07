from pathlib import Path
from unittest.mock import MagicMock

import pytest

from issue_creator_kit.usecase.roadmap_sync import RoadmapSyncUseCase


@pytest.fixture
def mock_fs():
    return MagicMock()


@pytest.fixture
def usecase(mock_fs):
    return RoadmapSyncUseCase(mock_fs)


def test_sync_roadmap_success(usecase, mock_fs, tmp_path):
    # Setup
    roadmap_file = tmp_path / "roadmap.md"
    original_content = (
        "| ID | Task | File |\n"
        "| --- | --- | --- |\n"
        "| T1-1 | Task 1 | [issue-T1-1.md](../../tasks/drafts/phase-1/issue-T1-1.md) |\n"
        "| T1-2 | Task 2 | [issue-T1-2.md](../../tasks/drafts/phase-1/issue-T1-2.md) |\n"
    )
    roadmap_file.write_text(original_content, encoding="utf-8")
    mock_fs.read_file.return_value = original_content

    results = [
        (Path("reqs/tasks/archive/phase-1/issue-T1-1.md"), 101),
        (Path("reqs/tasks/archive/phase-1/issue-T1-2.md"), 102),
    ]

    # Execute
    usecase.sync(str(roadmap_file), results)

    # Verify
    mock_fs.read_file.assert_called_with(str(roadmap_file))
    # Check what was written back
    write_call = mock_fs.write_file.call_args
    new_content = write_call.args[1]

    assert "../../tasks/archive/phase-1/issue-T1-1.md" in new_content
    assert (
        "[issue-T1-1.md](../../tasks/archive/phase-1/issue-T1-1.md) (#101)"
        in new_content
    )
    assert "../../tasks/archive/phase-1/issue-T1-2.md" in new_content
    assert (
        "[issue-T1-2.md](../../tasks/archive/phase-1/issue-T1-2.md) (#102)"
        in new_content
    )
    assert "drafts" not in new_content


def test_sync_roadmap_missing_link_raises_error(usecase, mock_fs, tmp_path):
    # Setup
    roadmap_file = tmp_path / "roadmap.md"
    original_content = (
        "| ID | Task | File |\n"
        "| --- | --- | --- |\n"
        "| T1-1 | Task 1 | [wrong-file.md](../../tasks/drafts/phase-1/wrong-file.md) |\n"
    )
    roadmap_file.write_text(original_content, encoding="utf-8")
    mock_fs.read_file.return_value = original_content

    results = [(Path("reqs/tasks/archive/phase-1/issue-T1-1.md"), 101)]

    # Execute & Verify
    with pytest.raises(ValueError, match="Link for issue-T1-1.md not found in roadmap"):
        usecase.sync(str(roadmap_file), results)

    mock_fs.write_file.assert_not_called()


def test_sync_roadmap_no_changes(usecase, mock_fs, tmp_path):
    # Setup
    roadmap_file = tmp_path / "roadmap.md"
    original_content = "| ID | Task | File |\n| --- | --- | --- |\n"
    roadmap_file.write_text(original_content, encoding="utf-8")
    mock_fs.read_file.return_value = original_content

    # Execute (empty results)
    usecase.sync(str(roadmap_file), [])

    # Verify
    mock_fs.write_file.assert_not_called()


def test_sync_roadmap_duplicate_files(usecase, mock_fs, tmp_path):
    # Setup
    roadmap_file = tmp_path / "roadmap.md"
    content = "| T1-1 | [file.md](../../tasks/drafts/p1/file.md) |"
    roadmap_file.write_text(content, encoding="utf-8")
    mock_fs.read_file.return_value = content

    results = [
        (Path("reqs/tasks/archive/p1/file.md"), 101),
        (Path("reqs/tasks/archive/p1/file.md"), 101),  # Duplicate
    ]

    # Execute
    usecase.sync(str(roadmap_file), results)

    # Verify: Should only call write_file once despite duplicate in results
    assert mock_fs.write_file.call_count == 1


def test_sync_roadmap_robust_replacement(usecase, mock_fs, tmp_path):
    # Setup
    roadmap_file = tmp_path / "roadmap.md"
    # Mix of relative and absolute-like paths, some already archived
    original_content = (
        "- [task1.md](../../tasks/drafts/phase-1/task1.md)\n"
        "- [task2.md](drafts/task2.md)\n"
        "- [task3.md](../../tasks/archive/phase-0/task3.md) (#99)\n"
    )
    roadmap_file.write_text(original_content, encoding="utf-8")
    mock_fs.read_file.return_value = original_content

    results = [
        (Path("reqs/tasks/archive/phase-1/task1.md"), 101),
        (Path("reqs/tasks/archive/task2.md"), 102),
        (Path("reqs/tasks/archive/phase-0/task3.md"), 99),
    ]

    # Execute
    usecase.sync(str(roadmap_file), results)

    # Verify
    write_call = mock_fs.write_file.call_args
    new_content = write_call.args[1]

    assert "[task1.md](../../tasks/archive/phase-1/task1.md) (#101)" in new_content
    assert "[task2.md](archive/task2.md) (#102)" in new_content
    assert "[task3.md](../../tasks/archive/phase-0/task3.md) (#99)" in new_content
