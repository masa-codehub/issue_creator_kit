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
    def read_document(self, file_path: Path) -> Document:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        content = file_path.read_text(encoding="utf-8")
        return Document.parse(content)

    def save_document(
        self, file_path: Path, document: Document, use_frontmatter: bool = True
    ) -> None:
        content = document.to_string(use_frontmatter=use_frontmatter)
        file_path.write_text(content, encoding="utf-8")

    def update_metadata(self, file_path: Path, updates: dict[str, Any]) -> None:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        # Locking logic for concurrent safety
        if HAS_FCNTL:
            with open(file_path, "r+", encoding="utf-8") as f:
                fcntl.flock(f, fcntl.LOCK_EX)
                content = f.read()
                doc = Document.parse(content)

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
        self, src_path: Path, dst_dir: Path, overwrite: bool = False
    ) -> Path:
        if not src_path.exists():
            raise FileNotFoundError(f"Source file not found: {src_path}")

        dst_dir.mkdir(parents=True, exist_ok=True)
        dst_path = dst_dir / src_path.name

        if dst_path.exists() and not overwrite:
            raise FileExistsError(f"Destination file exists: {dst_path}")

        shutil.move(str(src_path), str(dst_path))
        return dst_path

    def list_files(self, dir_path: Path, pattern: str = "*") -> list[Path]:
        if not dir_path.exists():
            return []
        return list(dir_path.glob(pattern))

    def read_file(self, path: Path | str) -> str:
        return Path(path).read_text(encoding="utf-8")

    def write_file(self, path: Path | str, content: str) -> None:
        Path(path).write_text(content, encoding="utf-8")
