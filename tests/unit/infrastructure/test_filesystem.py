from pathlib import Path

import pytest

from issue_creator_kit.domain.document import Document, Metadata
from issue_creator_kit.domain.exceptions import FileSystemError
from issue_creator_kit.domain.interfaces import IFileSystemAdapter
from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter


class TestFileSystemAdapter:
    @pytest.fixture
    def adapter(self):
        return FileSystemAdapter()

    def test_protocol_conformance(self, adapter):
        assert isinstance(adapter, IFileSystemAdapter)

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

    def test_find_file_by_id_success(self, adapter, fs):
        # Setup mock files in multiple dirs
        fs.create_file(
            "dir1/task1.md",
            contents="---\nid: task-001\nstatus: Draft\ntitle: Task 1\n---\nBody 1",
        )
        fs.create_file(
            "dir2/task2.md",
            contents="---\nid: task-002\nstatus: Draft\ntitle: Task 2\n---\nBody 2",
        )
        fs.create_file(
            "dir2/other.md",
            contents="---\nid: task-003\nstatus: Draft\ntitle: Other\n---\nBody 3",
        )

        # Search in dir2
        path = adapter.find_file_by_id("task-002", ["dir1", "dir2"])
        assert path == Path("dir2/task2.md")

        # Search in dir1
        path = adapter.find_file_by_id("task-001", ["dir1", "dir2"])
        assert path == Path("dir1/task1.md")

    def test_find_file_by_id_not_found(self, adapter, fs):
        fs.create_file(
            "dir1/task1.md",
            contents="---\nid: task-001\nstatus: Draft\ntitle: Task 1\n---\nBody 1",
        )

        with pytest.raises(FileSystemError) as excinfo:
            adapter.find_file_by_id("task-999", ["dir1"])
        assert "task-999" in str(excinfo.value)
