from pathlib import Path

from ragline.index import build_index
from ragline.retrieve import retrieve


def test_hybrid_retrieves_hybrid_doc():
    root = Path(__file__).resolve().parents[3] / "sample_docs"
    idx = build_index(sorted(root.glob("*.md")))
    hits = retrieve(idx, "What is reciprocal rank fusion hybrid retrieval?", top_k=3)
    assert hits
    blob = " ".join(h.chunk.text.lower() for h in hits)
    assert "hybrid" in blob or "bm25" in blob or "fusion" in blob
