#!/usr/bin/env python3
"""Index sample_docs and print retrieved citations."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "packages" / "ragline" / "src"))

from ragline.index import build_index, save_index
from ragline.retrieve import pack_citations, retrieve


def main() -> None:
    docs = ROOT / "sample_docs"
    out = ROOT / ".ragline_index"
    idx = build_index(sorted(docs.glob("*.md")))
    save_index(idx, out)
    q = " ".join(sys.argv[1:]) or "What is hybrid retrieval and RRF?"
    print(pack_citations(retrieve(idx, q, top_k=4)))


if __name__ == "__main__":
    main()
