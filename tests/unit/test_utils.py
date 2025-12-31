from pathlib import Path

import pytest

from issue_creator_kit.utils import (
    load_document,
    safe_move_file,
    save_document,
    update_metadata,
)


def test_load_document_standard(tmp_path: Path):
    """L-1: 標準的な Frontmatter の読み込み"""
    file_path = tmp_path / "test.md"
    content = "---\ntitle: Test\n---\n# Body"
    file_path.write_text(content, encoding="utf-8")

    metadata, body = load_document(file_path)
    assert metadata == {"title": "Test"}
    assert body.strip() == "# Body"


def test_load_document_markdown_list(tmp_path: Path):
    """L-2: Markdown リスト形式のメタデータの読み込み"""
    file_path = tmp_path / "test.md"
    content = "# Summary\n\n- **Status**: 提案中\n- **Date**: 2025-12-31\n\nBody"
    file_path.write_text(content, encoding="utf-8")

    metadata, body = load_document(file_path)
    assert metadata == {"Status": "提案中", "Date": "2025-12-31"}
    assert "Body" in body


def test_load_document_no_frontmatter(tmp_path: Path):
    """L-3: メタデータなしのドキュメント"""
    file_path = tmp_path / "test.md"
    content = "# Body Only"
    file_path.write_text(content, encoding="utf-8")

    metadata, body = load_document(file_path)
    assert metadata == {}
    assert body.strip() == "# Body Only"


def test_load_document_file_not_found():
    """L-E1: ファイルが見つからない場合のエラー"""
    with pytest.raises(FileNotFoundError):
        load_document(Path("non_existent_file.md"))


def test_save_document_new(tmp_path: Path):
    """U-1: 新規保存（Frontmatter形式）"""
    file_path = tmp_path / "new.md"
    metadata = {"title": "New"}
    content = "Body content"

    save_document(file_path, metadata, content)

    assert file_path.exists()
    metadata_loaded, body_loaded = load_document(file_path)
    assert metadata_loaded == metadata
    assert body_loaded.strip() == content


def test_update_metadata_existing_frontmatter(tmp_path: Path):
    """U-2: Frontmatter 形式の更新"""
    file_path = tmp_path / "test.md"
    file_path.write_text("---\ntitle: Old\n---\nBody", encoding="utf-8")

    update_metadata(file_path, {"title": "New"})

    metadata, body = load_document(file_path)
    assert metadata["title"] == "New"
    assert body.strip() == "Body"


def test_update_metadata_markdown_list(tmp_path: Path):
    """U-3: Markdown リスト形式の更新"""
    file_path = tmp_path / "test.md"
    content = "# Summary\n\n- **Status**: 提案中\n\nBody"
    file_path.write_text(content, encoding="utf-8")

    update_metadata(file_path, {"Status": "承認済み", "Issue": "#123"})

    metadata, body = load_document(file_path)
    assert metadata["Status"] == "承認済み"
    assert metadata["Issue"] == "#123"
    assert "Body" in body


def test_save_document_multibyte(tmp_path: Path):
    """U-4: マルチバイト文字の扱い"""
    file_path = tmp_path / "test.md"
    metadata = {"title": "テスト"}
    content = "本文"

    save_document(file_path, metadata, content)

    text = file_path.read_text(encoding="utf-8")
    assert (
        "title: テスト" in text
        or 'title: "\\u30c6\\u30b9\\u30c8"' in text
        or "title: \u30c6\u30b9\u30c8" in text
    )
    assert "本文" in text


def test_safe_move_file_success(tmp_path: Path):
    """S-1: ファイルの移動成功"""
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
    """S-2: 上書き移動"""
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
