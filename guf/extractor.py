"""Core logic for guf (Git URL in Files)."""

from __future__ import annotations

import os
import re
from pathlib import Path
from typing import Iterable

URL_PATTERN = re.compile(
    r"""
    (?:
        (?P<scheme>https?|ftp|git|ssh)://[^\s"'<>()\[\]{}]+
        |
        git@[^\s"'<>()\[\]{}:]+:[^\s"'<>()\[\]{}]+
    )
    """,
    re.VERBOSE | re.IGNORECASE,
)

DEFAULT_EXTENSIONS = {
    ".txt", ".md", ".rst", ".py", ".js", ".ts", ".jsx", ".tsx",
    ".json", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf",
    ".env", ".sh", ".bash", ".zsh", ".html", ".css", ".xml",
    ".java", ".c", ".cpp", ".h", ".hpp", ".go", ".rs", ".rb",
    ".php", ".sql", ".gitconfig", ".dockerfile",
}


def extract_urls(text: str) -> list[str]:
    """استخرج كل الروابط من نص معين."""
    if not text:
        return []
    results = []
    for m in URL_PATTERN.finditer(text):
        url = m.group(0).rstrip(".,;:!?)]}\"'")
        results.append(url)
    return results


def extract_from_file(path: str | Path, encoding: str = "utf-8") -> list[str]:
    """استخرج الروابط من ملف واحد."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"File not found: {p}")
    try:
        content = p.read_text(encoding=encoding, errors="ignore")
    except Exception as e:
        raise RuntimeError(f"Failed reading {p}: {e}") from e
    return extract_urls(content)


def extract_from_directory(
    directory: str | Path,
    recursive: bool = True,
    extensions: Iterable[str] | None = None,
    skip_hidden: bool = True,
    max_size_mb: float = 5.0,
) -> dict[str, list[str]]:
    """استخرج الروابط من كل الملفات داخل مجلد."""
    root = Path(directory)
    if not root.is_dir():
        raise NotADirectoryError(f"Not a directory: {root}")

    allowed_exts = set(extensions) if extensions else None
    max_bytes = int(max_size_mb * 1024 * 1024)
    results: dict[str, list[str]] = {}

    walker = root.rglob("*") if recursive else root.glob("*")

    for path in walker:
        if not path.is_file():
            continue

        if skip_hidden and any(part.startswith(".") for part in path.parts):
            if path.name not in {".gitconfig", ".env"}:
                continue

        try:
            if path.stat().st_size > max_bytes:
                continue
        except OSError:
            continue

        if allowed_exts is not None:
            if path.suffix.lower() not in allowed_exts and path.name.lower() not in allowed_exts:
                continue

        try:
            urls = extract_from_file(path)
        except Exception:
            continue

        if urls:
            results[str(path)] = urls

    return results
