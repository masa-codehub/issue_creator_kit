from pathlib import Path

import pytest

from issue_creator_kit.domain.document import Document, Metadata
from issue_creator_kit.domain.exceptions import FileSystemError
from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter


class TestFileSystemAdapter:
    @pytest.fixture
    def adapter(self):
        return FileSystemAdapter()

    def test_protocol_conformance(self, adapter):
        # Verify that the adapter implements the required methods from IFileSystemAdapter
        required_methods = (
            "read_document",
            "save_document",
            "update_metadata",
            "list_files",
            "find_file_by_id",
        )
        for name in required_methods:
            assert hasattr(adapter, name)

    def test_read_document_success(self, adapter, tmp_path):
        # F-1: Read document with correct separation
        file_path = tmp_path / "test.md"
        file_path.write_text(
            "---\nid: test-doc\nstatus: Draft\ntitle: Test\n---\n# Content",
            encoding="utf-8",
        )

        doc = adapter.read_document(file_path)
        assert doc.metadata["id"] == "test-doc"
        assert doc.metadata["status"] == "Draft"
        assert doc.content == "# Content"

    def test_read_document_parse_error(self, adapter, tmp_path):
        # F-2: Parse error (Document.parse behavior)
        # Invalid YAML that results in ValidationError because required fields missing
        file_path = tmp_path / "bad.md"
        file_path.write_text("---\ntitle: : bad\n---\nContent", encoding="utf-8")

        from issue_creator_kit.domain.exceptions import ValidationError

        with pytest.raises(ValidationError):
            adapter.read_document(file_path)

    def test_save_document_new(self, adapter, tmp_path):
        # F-3: Save new document
        file_path = tmp_path / "new.md"
        metadata = Metadata(id="new-doc", status="Draft", title="New")
        doc = Document(metadata=metadata, content="Body")
        adapter.save_document(file_path, doc)

        assert file_path.exists()
        content = file_path.read_text(encoding="utf-8")
        assert "id: new-doc" in content
        assert "status: Draft" in content
        assert "Body" in content

    def test_update_metadata_preserves_content(self, adapter, tmp_path):
        # F-4: Update metadata only
        file_path = tmp_path / "update.md"
        file_path.write_text(
            "---\nid: update-doc\nstatus: Draft\n---\nBody", encoding="utf-8"
        )

        # In update_metadata, we pass a dict of updates
        adapter.update_metadata(file_path, {"status": "Ready", "added": 1})

        content = file_path.read_text(encoding="utf-8")
        assert "id: update-doc" in content
        assert "status: Ready" in content
        assert "added: 1" in content
        assert "Body" in content
        assert "status: Draft" not in content

    def test_safe_move_file_success(self, adapter, tmp_path):
        # F-5: Move file success
        src = tmp_path / "src.md"
        src.touch()
        dst_dir = tmp_path / "dst"

        new_path_str = adapter.safe_move_file(src, dst_dir)
        new_path = Path(new_path_str)

        assert not src.exists()
        assert new_path.exists()
        assert new_path.parent == dst_dir
        assert new_path.name == "src.md"

    def test_safe_move_file_exists_error(self, adapter, tmp_path):
        # F-6: Move destination exists error
        src = tmp_path / "src.md"
        src.touch()
        dst_dir = tmp_path / "dst"
        dst_dir.mkdir()
        (dst_dir / "src.md").touch()

        with pytest.raises(FileExistsError):
            adapter.safe_move_file(src, dst_dir, overwrite=False)

    def test_safe_move_file_overwrite(self, adapter, tmp_path):
        # F-6 variant: Overwrite
        src = tmp_path / "src.md"
        src.write_text("new")
        dst_dir = tmp_path / "dst"
        dst_dir.mkdir()
        dst = dst_dir / "src.md"
        dst.write_text("old")

        adapter.safe_move_file(src, dst_dir, overwrite=True)

        assert dst.read_text() == "new"

    def test_find_file_by_id_success(self, adapter, tmp_path):
        # Setup mock files in multiple dirs
        dir1 = tmp_path / "dir1"
        dir1.mkdir()
        dir2 = tmp_path / "dir2"
        dir2.mkdir()

        f1 = dir1 / "task1.md"
        f1.write_text(
            "---\nid: task-001\nstatus: Draft\ntitle: Task 1\n---\nBody 1",
            encoding="utf-8",
        )
        f2 = dir2 / "task2.md"
        f2.write_text(
            "---\n  id  :   task-002  \nstatus: Draft\ntitle: Task 2\n---\nBody 2",
            encoding="utf-8",
        )
        f3 = dir2 / "other.md"
        f3.write_text(
            "---\nid: 'task-003'\nstatus: Draft\ntitle: Other\n---\nBody 3",
            encoding="utf-8",
        )

        # Search in dir2
        path = adapter.find_file_by_id("task-002", [str(dir1), str(dir2)])
        assert path.resolve() == f2.resolve()

        # Search in dir1
        path = adapter.find_file_by_id("task-001", [str(dir1), str(dir2)])
        assert path.resolve() == f1.resolve()

        # Search with quotes
        path = adapter.find_file_by_id("task-003", [str(dir2)])
        assert path.resolve() == f3.resolve()

    def test_find_file_by_id_edge_cases(self, adapter, tmp_path):
        # 1. Special characters in ID
        dir1 = tmp_path / "dir1"
        dir1.mkdir()
        f1 = dir1 / "special.md"
        f1.write_text("---\nid: task-special(draft)\n---\nBody", encoding="utf-8")

        path = adapter.find_file_by_id("task-special(draft)", [str(dir1)])
        assert path.resolve() == f1.resolve()

        # 2. Empty search_dirs
        with pytest.raises(FileSystemError):
            adapter.find_file_by_id("any", [])

        # 3. Multiple files with same ID (returns first found)
        dir2 = tmp_path / "dir2"
        dir2.mkdir()
        f2 = dir2 / "task_dup.md"
        f2.write_text("---\nid: task-dup\n---\nBody", encoding="utf-8")
        f3 = dir1 / "task_dup_other.md"
        f3.write_text("---\nid: task-dup\n---\nBody", encoding="utf-8")

        # In dir1, dir2 order -> finds f3
        path = adapter.find_file_by_id("task-dup", [str(dir1), str(dir2)])
        assert path.resolve() == f3.resolve()

        # In dir2, dir1 order -> finds f2
        path = adapter.find_file_by_id("task-dup", [str(dir2), str(dir1)])
        assert path.resolve() == f2.resolve()

    def test_find_file_by_id_not_found(self, adapter, tmp_path):
        dir1 = tmp_path / "dir1"
        dir1.mkdir()
        (dir1 / "task1.md").write_text("---\nid: task-001\n---\nBody", encoding="utf-8")

        with pytest.raises(FileSystemError) as excinfo:
            adapter.find_file_by_id("task-999", [str(dir1)])
        assert "task-999" in str(excinfo.value)
