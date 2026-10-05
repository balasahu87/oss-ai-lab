# ragline

Hybrid **RAG** toolkit: chunking, BM25 + dense retrieval, Reciprocal Rank Fusion,
citation packing, and a small CLI.

```bash
pip install -e .
ragline index ./docs --out .ragline_index
ragline ask "What is RRF?" --index .ragline_index
```

Offline by default (hashing embedder). Swap in a real embedding model later
via the `Embedder` protocol.
