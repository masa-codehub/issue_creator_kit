import re
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
    YAML Frontmatter または Markdown リスト形式のメタデータを含む Markdown ドキュメントを読み込みます。

    Args:
        file_path (Path): 読み込むファイルのパス。

    Returns:
        tuple[dict[str, Any], str]: メタデータ（辞書）と本文（文字列）のタプル。

    Raises:
        FileNotFoundError: ファイルが存在しない場合。
        yaml.YAMLError: フロントマターの解析に失敗した場合。
    """
    if not file_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    content = file_path.read_text(encoding="utf-8")

    # 1. YAML Frontmatter を試行
    if content.startswith("---"):
        post = frontmatter.loads(content)
        return dict(post.metadata), post.content

    # 2. Markdown リスト形式 (- **Key**: Value) を試行
    metadata = {}
    metadata_pattern = re.compile(r"^- \*\*([^*]+)\*\*: (.*)$")

    lines = content.splitlines()
    body_start_idx = 0
    metadata_found = False

    for i, line in enumerate(lines):
        match = metadata_pattern.match(line)
        if match:
            key, value = match.groups()
            metadata[key] = value
            metadata_found = True
            body_start_idx = i + 1
        elif metadata_found and not line.strip():
            body_start_idx = i + 1
        elif metadata_found or i > 15:
            break

    if metadata:
        body = "\n".join(lines[body_start_idx:])
        return metadata, body
    return {}, content


def save_document(file_path: Path, metadata: dict[str, Any], content: str) -> None:
    """
    Markdown ドキュメントを保存します。
    既存のファイルがある場合、その形式（YAML Frontmatter または Markdown リスト形式）を維持します。

    Args:
        file_path (Path): 保存先のパス。
        metadata (dict[str, Any]): メタデータの辞書。
        content (str): ファイルの本文。

    Raises:
        PermissionError: 権限不足でファイルが書き込めない場合。
        OSError: ファイル書き込み中にOSレベルのエラーが発生した場合。
        Exception: フロントマターまたはコンテンツのシリアライズに失敗した場合。
    """
    use_frontmatter = True
    if file_path.exists():
        orig_content = file_path.read_text(encoding="utf-8")
        if orig_content and not orig_content.startswith("---"):
            use_frontmatter = False

    if use_frontmatter:
        post = frontmatter.Post(content, **metadata)
        text = frontmatter.dumps(post)
    else:
        # Markdown リスト形式を維持
        metadata_lines = [f"- **{key}**: {value}" for key, value in metadata.items()]
        lines = content.splitlines()
        header_line_idx = -1
        for i, line in enumerate(lines):
            if line.startswith("# "):
                header_line_idx = i
                break

        body_lines = [
            line for line in lines if not re.match(r"^- \*\*([^*]+)\*\*: (.*)$", line)
        ]

        if header_line_idx != -1:
            new_content = []
            inserted = False
            for i, line in enumerate(body_lines):
                new_content.append(line)
                if not inserted and (
                    i == header_line_idx
                    or (i == header_line_idx + 1 and body_lines[i].strip())
                ):
                    if i + 1 < len(body_lines) and not body_lines[i + 1].strip():
                        continue
                    new_content.append("")
                    new_content.extend(metadata_lines)
                    new_content.append("")
                    inserted = True
            text = "\n".join(new_content)
        else:
            text = "\n".join(metadata_lines) + "\n\n" + "\n".join(body_lines)

    file_path.write_text(text, encoding="utf-8")


def update_metadata(file_path: Path, updates: dict[str, Any]) -> None:
    """
    既存の Markdown ドキュメントのメタデータを更新します。

    Args:
        file_path (Path): 更新対象のファイルのパス。
        updates (dict[str, Any]): 更新するメタデータの辞書（部分更新）。

    Raises:
        FileNotFoundError: ファイルが存在しない場合。
        yaml.YAMLError: 既存ドキュメントの読み込みまたは解析に失敗した場合。
        OSError: 更新されたドキュメントのディスクへの書き込みに失敗した場合。
    """
    if not file_path.exists():
        raise FileNotFoundError(f"ファイルが見つかりません: {file_path}")

    if HAS_FCNTL:
        with open(file_path, "r+", encoding="utf-8") as f:
            fcntl.flock(f, fcntl.LOCK_EX)
            orig_content = f.read()
            f.seek(0)

            if orig_content.startswith("---"):
                post = frontmatter.loads(orig_content)
                post.metadata.update(updates)
                text = frontmatter.dumps(post)
            else:
                metadata, body = load_document(file_path)
                metadata.update(updates)
                metadata_lines = [
                    f"- **{key}**: {value}" for key, value in metadata.items()
                ]
                lines = body.splitlines()
                header_line_idx = -1
                for i, line in enumerate(lines):
                    if line.startswith("# "):
                        header_line_idx = i
                        break
                body_lines = [
                    line
                    for line in lines
                    if not re.match(r"^- \*\*([^*]+)\*\*: (.*)$", line)
                ]
                if header_line_idx != -1:
                    new_content = []
                    inserted = False
                    for i, line in enumerate(body_lines):
                        new_content.append(line)
                        if not inserted and (
                            i == header_line_idx
                            or (i == header_line_idx + 1 and body_lines[i].strip())
                        ):
                            if (
                                i + 1 < len(body_lines)
                                and not body_lines[i + 1].strip()
                            ):
                                continue
                            new_content.append("")
                            new_content.extend(metadata_lines)
                            new_content.append("")
                            inserted = True
                    text = "\n".join(new_content)
                else:
                    text = "\n".join(metadata_lines) + "\n\n" + body

            f.seek(0)
            f.truncate()
            f.write(text)
    else:
        metadata, content = load_document(file_path)
        metadata.update(updates)
        save_document(file_path, metadata, content)


def safe_move_file(src_path: Path, dst_dir: Path, overwrite: bool = False) -> Path:
    """
    ファイルを安全に移動します。

    Args:
        src_path (Path): 移動元のパス。
        dst_dir (Path): 移動先のディレクトリパス。
        overwrite (bool): 上書きを許可するかどうか。

    Returns:
        Path: 移動後のファイルパス。

    Raises:
        FileNotFoundError: 移動元が存在しない場合。
        FileExistsError: 移動先が既に存在し、overwrite が False の場合。
    """
    if not src_path.exists():
        raise FileNotFoundError(f"移動元のファイルが見つかりません: {src_path}")

    dst_dir.mkdir(parents=True, exist_ok=True)
    dst_path = dst_dir / src_path.name

    if dst_path.exists() and not overwrite:
        raise FileExistsError(f"移動先のファイルが既に存在します: {dst_path}")

    shutil.move(src_path, dst_path)
    return dst_path
