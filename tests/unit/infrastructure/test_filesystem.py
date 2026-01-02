import pytest

from issue_creator_kit.domain.document import Document
from issue_creator_kit.infrastructure.filesystem import FileSystemAdapter


class TestFileSystemAdapter:
    @pytest.fixture
    def adapter(self):
        return FileSystemAdapter()

    def test_read_document_success(self, adapter, tmp_path):
        # F-1: Read document with correct separation
        file_path = tmp_path / "test.md"
        file_path.write_text("---\ntitle: Test\n---\n# Content", encoding="utf-8")

        doc = adapter.read_document(file_path)
        assert doc.metadata["title"] == "Test"
        assert doc.content == "# Content"

    def test_read_document_parse_error(self, adapter, tmp_path):
        # F-2: Parse error (Document.parse behavior)
        # Document.parse catches YAML errors and falls back to plain text/markdown list
        file_path = tmp_path / "bad.md"
        file_path.write_text("---\ntitle: : bad\n---\nContent", encoding="utf-8")

        doc = adapter.read_document(file_path)

        # Expectation: YAML parse fails, metadata empty, content contains raw text
        assert doc.metadata == {}
        assert "title: : bad" in doc.content

    def test_save_document_new(self, adapter, tmp_path):
        # F-3: Save new document
        file_path = tmp_path / "new.md"
        doc = Document(metadata={"title": "New"}, content="Body")
        adapter.save_document(file_path, doc)

        assert file_path.exists()
        content = file_path.read_text(encoding="utf-8")
        assert "title: New" in content
        assert "Body" in content

    def test_update_metadata_preserves_content(self, adapter, tmp_path):
        # F-4: Update metadata only
        file_path = tmp_path / "update.md"
        file_path.write_text("---\nstatus: old\n---\nBody", encoding="utf-8")

        adapter.update_metadata(file_path, {"status": "new", "added": 1})

        content = file_path.read_text(encoding="utf-8")
        assert "status: new" in content
        assert "added: 1" in content
        assert "Body" in content
        # Ensure 'old' status is gone
        assert "status: old" not in content

    def test_safe_move_file_success(self, adapter, tmp_path):
        # F-5: Move file success
        src = tmp_path / "src.md"
        src.touch()
        dst_dir = tmp_path / "dst"

        new_path = adapter.safe_move_file(src, dst_dir)

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
