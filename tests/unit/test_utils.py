from pathlib import Path

import frontmatter
import pytest
import yaml

from issue_creator_kit.utils import (
    load_document,
    safe_move_file,
    save_document,
    update_metadata,
)

# --- load_document Tests ---


def test_load_document_standard(tmp_path: Path):
    """L-1: Standard Frontmatter"""
    file_path = tmp_path / "test.md"
    content = "---\ntitle: Test\n---\n# Body"
    file_path.write_text(content, encoding="utf-8")

    metadata, body = load_document(file_path)
    assert metadata == {"title": "Test"}
    assert body.strip() == "# Body"


def test_load_document_no_frontmatter(tmp_path: Path):
    """L-2: No Frontmatter"""
    file_path = tmp_path / "test.md"
    content = "# Body Only"
    file_path.write_text(content, encoding="utf-8")

    metadata, body = load_document(file_path)
    assert metadata == {}
    assert body.strip() == "# Body Only"


def test_load_document_complex_types(tmp_path: Path):
    """L-3: Complex Types"""
    file_path = tmp_path / "test.md"
    content = "---\ntags: [a, b]\ncount: 1\n---\n"
    file_path.write_text(content, encoding="utf-8")

    metadata, body = load_document(file_path)
    assert metadata == {"tags": ["a", "b"], "count": 1}
    assert body.strip() == ""


def test_load_document_empty_frontmatter(tmp_path: Path):
    """L-4: Empty Frontmatter"""
    file_path = tmp_path / "test.md"
    content = "---\n---\nBody"
    file_path.write_text(content, encoding="utf-8")

    metadata, body = load_document(file_path)
    assert metadata == {}
    assert body.strip() == "Body"


def test_load_document_file_not_found():
    """L-E1: File Not Found"""
    with pytest.raises(FileNotFoundError):
        load_document(Path("non_existent_file.md"))


def test_load_document_invalid_yaml(tmp_path: Path):
    """L-E2: Invalid YAML"""
    file_path = tmp_path / "test.md"
    content = "---\nkey: : value\n---\n"
    file_path.write_text(content, encoding="utf-8")

    with pytest.raises(yaml.YAMLError):
        load_document(file_path)


# --- save_document / update_metadata Tests ---


def test_save_document_new(tmp_path: Path):
    """U-1: New Save"""
    file_path = tmp_path / "new.md"
    metadata = {"title": "New"}
    content = "Body content"

    save_document(file_path, metadata, content)

    assert file_path.exists()
    loaded = frontmatter.load(file_path)
    assert loaded.metadata == metadata
    assert loaded.content.strip() == content


def test_update_metadata_existing(tmp_path: Path):
    """U-2: Update Metadata"""
    file_path = tmp_path / "test.md"
    file_path.write_text("---\ntitle: Old\n---\nBody", encoding="utf-8")

    update_metadata(file_path, {"title": "New"})

    loaded = frontmatter.load(file_path)
    assert loaded.metadata["title"] == "New"
    assert loaded.content.strip() == "Body"


def test_update_metadata_add_key(tmp_path: Path):
    """U-3: Add Key"""
    file_path = tmp_path / "test.md"
    file_path.write_text("---\ntitle: Old\n---\nBody", encoding="utf-8")

    update_metadata(file_path, {"status": "Draft"})

    loaded = frontmatter.load(file_path)
    assert loaded.metadata["title"] == "Old"
    assert loaded.metadata["status"] == "Draft"


def test_save_document_types(tmp_path: Path):
    """U-4: Type Preservation"""
    file_path = tmp_path / "test.md"
    metadata = {"list": ["a", "b"], "int": 10}

    save_document(file_path, metadata, "")

    loaded = frontmatter.load(file_path)
    assert loaded.metadata["list"] == ["a", "b"]
    assert loaded.metadata["int"] == 10


def test_save_document_multibyte(tmp_path: Path):
    """U-E1: Multibyte characters"""
    file_path = tmp_path / "test.md"
    metadata = {"title": "テスト"}
    content = "本文"

    save_document(file_path, metadata, content)

    text = file_path.read_text(encoding="utf-8")
    assert "title: テスト" in text
    assert "本文" in text


def test_update_metadata_empty(tmp_path: Path):
    """U-E2: Empty Update"""
    file_path = tmp_path / "test.md"
    original_content = "---\ntitle: A\n---\nBody"
    file_path.write_text(original_content, encoding="utf-8")

    update_metadata(file_path, {})

    loaded = frontmatter.load(file_path)
    assert loaded.metadata == {"title": "A"}
    assert loaded.content.strip() == "Body"


# --- safe_move_file Tests ---


def test_safe_move_file_success(tmp_path: Path):
    """S-1: Success Move"""
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    dst_dir = tmp_path / "dst"

    src_file = src_dir / "test.md"
    src_file.write_text("content")

    new_path = safe_move_file(src_file, dst_dir)

    assert not src_file.exists()
    assert new_path.exists()
    assert new_path.parent == dst_dir
    assert new_path.name == "test.md"


def test_safe_move_file_overwrite(tmp_path: Path):
    """S-2: Overwrite"""
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    dst_dir = tmp_path / "dst"
    dst_dir.mkdir()

    src_file = src_dir / "test.md"
    src_file.write_text("new content")

    dst_file = dst_dir / "test.md"
    dst_file.write_text("old content")

    safe_move_file(src_file, dst_dir, overwrite=True)

    assert dst_file.read_text() == "new content"


def test_safe_move_file_not_found(tmp_path: Path):
    """S-E1: Source Not Found"""
    with pytest.raises(FileNotFoundError):
        safe_move_file(Path("non_existent"), tmp_path)


def test_safe_move_file_exists_error(tmp_path: Path):
    """S-E2: Destination Exists Error"""
    src_dir = tmp_path / "src"
    src_dir.mkdir()
    dst_dir = tmp_path / "dst"
    dst_dir.mkdir()

    src_file = src_dir / "test.md"
    src_file.write_text("new content")

    dst_file = dst_dir / "test.md"
    dst_file.write_text("old content")

    with pytest.raises(FileExistsError):
        safe_move_file(src_file, dst_dir, overwrite=False)
