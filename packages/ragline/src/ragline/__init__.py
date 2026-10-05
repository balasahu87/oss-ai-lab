"""ragline — hybrid RAG (BM25 + dense + RRF)."""

from ragline.chunk import Chunk, chunk_text
from ragline.index import Index, build_index, load_index, save_index
from ragline.retrieve import Retrieved, retrieve

__all__ = [
    "Chunk",
    "chunk_text",
    "Index",
    "build_index",
    "save_index",
    "load_index",
    "Retrieved",
    "retrieve",
]
__version__ = "0.1.0"
