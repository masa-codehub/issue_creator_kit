import shutil
from pathlib import Path
from typing import Any

import frontmatter


def load_document(file_path: Path) -> tuple[dict[str, Any], str]:
    """
    Load a Markdown document with YAML Frontmatter.

    Args:
        file_path (Path): Path to the markdown file.

    Returns:
        Tuple[Dict[str, Any], str]: A tuple containing the metadata (dict) and content (str).

    Raises:
        FileNotFoundError: If the file does not exist.
        Exception: If parsing fails (dependent on python-frontmatter/pyyaml).
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    post = frontmatter.load(file_path)
    return post.metadata, post.content


def save_document(file_path: Path, metadata: dict[str, Any], content: str) -> None:
    """
    Save a Markdown document with YAML Frontmatter.

    Args:
        file_path (Path): Path where the file will be saved.
        metadata (Dict[str, Any]): Dictionary of metadata to save as Frontmatter.
        content (str): The body content of the markdown file.
    """
    post = frontmatter.Post(content, **metadata)
    # dumps returns a string representation of the post
    text = frontmatter.dumps(post)
    file_path.write_text(text, encoding="utf-8")


def update_metadata(file_path: Path, updates: dict[str, Any]) -> None:
    """
    Update metadata of an existing Markdown document.

    Args:
        file_path (Path): Path to the existing file.
        updates (Dict[str, Any]): Dictionary of metadata updates (partial update).

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    metadata, content = load_document(file_path)
    metadata.update(updates)
    save_document(file_path, metadata, content)


def safe_move_file(src_path: Path, dst_dir: Path, overwrite: bool = False) -> Path:
    """
    Safely move a file to a destination directory.

    Args:
        src_path (Path): Path to the source file.
        dst_dir (Path): Path to the destination directory.
        overwrite (bool): Whether to overwrite the destination file if it exists.

    Returns:
        Path: The path to the moved file.

    Raises:
        FileNotFoundError: If src_path does not exist.
        FileExistsError: If destination exists and overwrite is False.
    """
    if not src_path.exists():
        raise FileNotFoundError(f"Source file not found: {src_path}")

    # Ensure destination directory exists
    dst_dir.mkdir(parents=True, exist_ok=True)

    dst_path = dst_dir / src_path.name

    if dst_path.exists() and not overwrite:
        raise FileExistsError(f"Destination file already exists: {dst_path}")

    # shutil.move handles overwrite if dst is a file, but we checked logic above.
    # If overwrite is True, shutil.move will overwrite.
    shutil.move(str(src_path), str(dst_path))

    return dst_path
