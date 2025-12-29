from pathlib import Path


def parse_metadata(content: str) -> dict[str, str]:
    """
    Extracts metadata from markdown content.

    Looks for lines starting with "- **Key**: Value" or "* **Key**: Value" at the beginning of lines.
    Supports both bold and non-bold keys.

    Args:
        content: The markdown string to parse.

    Returns:
        A dictionary containing the extracted metadata keys and values.
    """
    # Implementation will follow in Phase 2
    return {}


def update_metadata(content: str, updates: dict[str, str]) -> str:
    """
    Updates or adds metadata in markdown content.

    Identifies existing metadata using established regex patterns and replaces their values.
    If a key doesn't exist, it can be appended to the metadata section (TBD).

    Args:
        content: The original markdown string.
        updates: A dictionary of keys to update and their new values.

    Returns:
        The updated markdown string.
    """
    # Implementation will follow in Phase 2
    return content


def safe_move_file(src_path: Path, dst_dir: Path, overwrite: bool = False) -> Path:
    """
    Moves a file to a destination directory safely.

    Ensures the destination directory exists and handles potential name collisions.

    Args:
        src_path: Path to the source file.
        dst_dir: Path to the destination directory.
        overwrite: If True, overwrites existing file at destination.

    Returns:
        The new Path of the moved file.

    Raises:
        FileNotFoundError: If src_path does not exist.
        FileExistsError: If destination exists and overwrite is False.
    """
    # Implementation will follow in Phase 2
    return Path()
