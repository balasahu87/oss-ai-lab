from __future__ import annotations

from dataclasses import dataclass

from ragline.chunk import Chunk
from ragline.embed import Embedder, HashingEmbedder, cosine
from ragline.index import Index, bm25_scores


@dataclass
class Retrieved:
    chunk: Chunk
    score: float
    rank: int


def rrf_fuse(rank_lists: list[list[int]], k: int = 60) -> dict[int, float]:
    """Reciprocal Rank Fusion over lists of chunk indices (best-first)."""
    scores: dict[int, float] = {}
    for ranks in rank_lists:
        for r, idx in enumerate(ranks):
            scores[idx] = scores.get(idx, 0.0) + 1.0 / (k + r + 1)
    return scores


def retrieve(
    index: Index,
    query: str,
    *,
    top_k: int = 5,
    embedder: Embedder | None = None,
) -> list[Retrieved]:
    embedder = embedder or HashingEmbedder()
    bm25 = bm25_scores(index, query)
    bm25_order = sorted(range(len(bm25)), key=lambda i: bm25[i], reverse=True)

    qv = embedder.embed([query])[0]
    dense = [cosine(qv, v) for v in index.vectors] if index.vectors else [0.0] * len(index.chunks)
    dense_order = sorted(range(len(dense)), key=lambda i: dense[i], reverse=True)

    fused = rrf_fuse([bm25_order[:50], dense_order[:50]])
    ordered = sorted(fused.items(), key=lambda x: x[1], reverse=True)[:top_k]
    return [
        Retrieved(chunk=index.chunks[idx], score=score, rank=r)
        for r, (idx, score) in enumerate(ordered, start=1)
    ]


def pack_citations(hits: list[Retrieved], *, max_chars: int = 3500) -> str:
    parts: list[str] = []
    used = 0
    for h in hits:
        block = f"[{h.rank}] ({h.chunk.source})\n{h.chunk.text}\n"
        if used + len(block) > max_chars:
            break
        parts.append(block)
        used += len(block)
    return "\n".join(parts)
