from __future__ import annotations

import json
import math
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from ragline.chunk import Chunk, chunk_text, tokenize
from ragline.embed import Embedder, HashingEmbedder


@dataclass
class Index:
    chunks: list[Chunk]
    vectors: list[list[float]]
    # BM25 stats
    df: dict[str, int]
    doc_len: list[int]
    avgdl: float
    N: int


def build_index(
    paths: Iterable[Path],
    *,
    embedder: Embedder | None = None,
    chunk_size: int = 400,
    overlap: int = 60,
) -> Index:
    embedder = embedder or HashingEmbedder()
    chunks: list[Chunk] = []
    for path in paths:
        text = path.read_text(encoding="utf-8", errors="replace")
        chunks.extend(chunk_text(text, source=str(path), chunk_size=chunk_size, overlap=overlap))
    vectors = embedder.embed([c.text for c in chunks]) if chunks else []

    df: dict[str, int] = defaultdict(int)
    doc_len: list[int] = []
    for c in chunks:
        toks = tokenize(c.text)
        doc_len.append(len(toks))
        for t in set(toks):
            df[t] += 1
    N = len(chunks) or 1
    avgdl = (sum(doc_len) / N) if chunks else 0.0
    return Index(chunks=chunks, vectors=vectors, df=dict(df), doc_len=doc_len, avgdl=avgdl, N=N)


def save_index(index: Index, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    payload = {
        "chunks": [asdict(c) for c in index.chunks],
        "vectors": index.vectors,
        "df": index.df,
        "doc_len": index.doc_len,
        "avgdl": index.avgdl,
        "N": index.N,
    }
    (out_dir / "index.json").write_text(json.dumps(payload), encoding="utf-8")


def load_index(out_dir: Path) -> Index:
    data = json.loads((out_dir / "index.json").read_text(encoding="utf-8"))
    chunks = [Chunk(**c) for c in data["chunks"]]
    return Index(
        chunks=chunks,
        vectors=data["vectors"],
        df=data["df"],
        doc_len=data["doc_len"],
        avgdl=data["avgdl"],
        N=data["N"],
    )


def bm25_scores(index: Index, query: str, k1: float = 1.5, b: float = 0.75) -> list[float]:
    q_terms = tokenize(query)
    scores = [0.0] * len(index.chunks)
    if not q_terms:
        return scores
    q_tf = Counter(q_terms)
    for qi, tf_q in q_tf.items():
        n_qi = index.df.get(qi, 0)
        idf = math.log(1 + (index.N - n_qi + 0.5) / (n_qi + 0.5))
        for i, chunk in enumerate(index.chunks):
            toks = tokenize(chunk.text)
            tf = toks.count(qi)
            if tf == 0:
                continue
            dl = index.doc_len[i] or 1
            denom = tf + k1 * (1 - b + b * dl / (index.avgdl or 1))
            scores[i] += idf * (tf * (k1 + 1) / denom) * tf_q
    return scores
