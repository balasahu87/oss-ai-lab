from __future__ import annotations

import hashlib
import math
from typing import Protocol


class Embedder(Protocol):
    def embed(self, texts: list[str]) -> list[list[float]]: ...


class HashingEmbedder:
    """Deterministic bag-of-hashed-ngrams embedder (offline / CI friendly)."""

    def __init__(self, dim: int = 256):
        self.dim = dim

    def embed(self, texts: list[str]) -> list[list[float]]:
        out: list[list[float]] = []
        for text in texts:
            vec = [0.0] * self.dim
            tokens = text.lower().split()
            for i, tok in enumerate(tokens):
                for n in (tok, f"{tok}:{i % 7}"):
                    h = int(hashlib.md5(n.encode()).hexdigest(), 16)
                    vec[h % self.dim] += 1.0
                    vec[(h // self.dim) % self.dim] -= 0.25
            # L2 normalize
            norm = math.sqrt(sum(v * v for v in vec)) or 1.0
            out.append([v / norm for v in vec])
        return out


def cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))
