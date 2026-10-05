from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass
from typing import Iterable


@dataclass
class Chunk:
    id: str
    text: str
    source: str
    start: int
    end: int


def chunk_text(
    text: str,
    *,
    source: str = "",
    chunk_size: int = 400,
    overlap: int = 60,
) -> list[Chunk]:
    """Overlap character chunks; stable ids via content hash."""
    text = text.replace("\r\n", "\n").strip()
    if not text:
        return []
    chunks: list[Chunk] = []
    i = 0
    n = len(text)
    while i < n:
        end = min(n, i + chunk_size)
        # prefer break on paragraph/sentence
        if end < n:
            window = text[i:end]
            br = max(window.rfind("\n\n"), window.rfind(". "), window.rfind("\n"))
            if br > chunk_size // 3:
                end = i + br + 1
        piece = text[i:end].strip()
        if piece:
            digest = hashlib.sha1(f"{source}:{i}:{piece}".encode()).hexdigest()[:12]
            chunks.append(Chunk(id=digest, text=piece, source=source, start=i, end=end))
        if end >= n:
            break
        i = max(end - overlap, i + 1)
    return chunks


_TOKEN = re.compile(r"[a-z0-9]+", re.I)


def tokenize(text: str) -> list[str]:
    return [t.lower() for t in _TOKEN.findall(text or "")]
