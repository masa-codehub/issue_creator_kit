import shutil
from pathlib import Path
from typing import Any

from issue_creator_kit.domain.document import Document

try:
    import fcntl

    HAS_FCNTL = True
except ImportError:
    HAS_FCNTL = False


class FileSystemAdapter:
    def read_document(self, file_path: Path | str) -> Document:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = file_path.read_text(encoding="utf-8")
        return Document.parse(content, path=file_path)

    def save_document(
        self, file_path: Path | str, document: Document, use_frontmatter: bool = True
    ) -> None:
        file_path = Path(file_path)
        content = document.to_string(use_frontmatter=use_frontmatter)
        file_path.write_text(content, encoding="utf-8")

    def update_metadata(self, file_path: Path | str, updates: dict[str, Any]) -> None:
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Locking logic for concurrent safety
        if HAS_FCNTL:
            with open(file_path, "r+", encoding="utf-8") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                content = f.read()
                doc = Document.parse(content, path=file_path)

                # Check format preference based on existing content
                use_frontmatter = content.startswith("---")

                doc.metadata.update(updates)
                new_text = doc.to_string(use_frontmatter=use_frontmatter)

                f.seek(0)
                f.truncate()
                f.write(new_text)
        else:
            doc = self.read_document(file_path)
            # Check format preference
            content = file_path.read_text(encoding="utf-8")
            use_frontmatter = content.startswith("---")

            doc.metadata.update(updates)
            self.save_document(file_path, doc, use_frontmatter=use_frontmatter)

    def safe_move_file(
        self, src_path: Path | str, dst_dir: Path | str, overwrite: bool = False
    ) -> str:
        src_path = Path(src_path)
        dst_dir = Path(dst_dir)
        if not src_path.exists():
            raise FileNotFoundError(f"Source file not found: {src_path}")

        dst_dir.mkdir(parents=True, exist_ok=True)
        dst_path = dst_dir / src_path.name

        if dst_path.exists() and not overwrite:
            raise FileExistsError(f"Destination file exists: {dst_path}")

        shutil.move(str(src_path), str(dst_path))
        return str(dst_path)

    def list_files(self, dir_path: Path | str) -> list[str]:
        dir_path = Path(dir_path)
        if not dir_path.exists():
            return []
        return [str(f) for f in dir_path.iterdir() if f.is_file()]

    def read_file(self, path: Path | str) -> str:
        return Path(path).read_text(encoding="utf-8")

    def write_file(self, path: Path | str, content: str) -> None:
        Path(path).write_text(content, encoding="utf-8")

    def find_file_by_id(self, task_id: str, search_dirs: list[str]) -> Path:
        for d in search_dirs:
            p = Path(d)
            if not p.exists():
                continue
            for f in p.glob("*.md"):
                try:
                    doc = self.read_document(f)
                    if doc.metadata.id == task_id:
                        return f
                except Exception:
                    continue
        from issue_creator_kit.domain.exceptions import FileSystemError

        raise FileSystemError(f"File with id '{task_id}' not found in {search_dirs}")
