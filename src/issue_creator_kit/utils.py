import shutil
from pathlib import Path
from typing import Any

import frontmatter

try:
    import fcntl

    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False


def load_document(file_path: Path) -> tuple[dict[str, Any], str]:
    """
    Load a Markdown document with YAML Frontmatter.

    Args:
        file_path (Path): Path to the markdown file.

    Returns:
        tuple[dict[str, Any], str]: A tuple containing the metadata (dict) and content (str).

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If parsing the frontmatter fails.
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
        metadata (dict[str, Any]): Dictionary of metadata to save as Frontmatter.
        content (str): The body content of the markdown file.

    Raises:
        PermissionError: If the file cannot be written due to insufficient permissions.
        OSError: If an OS-level error occurs while writing the file.
        Exception: If serialization of the frontmatter or content fails.
    """
    post = frontmatter.Post(content, **metadata)
    text = frontmatter.dumps(post)
    file_path.write_text(text, encoding="utf-8")


def update_metadata(file_path: Path, updates: dict[str, Any]) -> None:
    """
    Update metadata of an existing Markdown document.

    Args:
        file_path (Path): Path to the existing file.
        updates (dict[str, Any]): Dictionary of metadata updates (partial update).

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If loading or parsing the existing document fails.
        OSError: If writing the updated document to disk fails.
    """
    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    if HAS_FCNTL:
        with open(file_path, "r+", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            post = frontmatter.load(f)
            post.metadata.update(updates)
            text = frontmatter.dumps(post)
            f.seek(0)
            f.truncate()
            f.write(text)
    else:
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

    dst_dir.mkdir(parents=True, exist_ok=True)

    dst_path = dst_dir / src_path.name

    if dst_path.exists() and not overwrite:
        raise FileExistsError(f"Destination file already exists: {dst_path}")

    shutil.move(src_path, dst_path)

    return dst_path
