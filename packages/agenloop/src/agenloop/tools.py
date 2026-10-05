from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from ragline.index import Index, load_index
from ragline.retrieve import pack_citations, retrieve


@dataclass
class Tool:
    name: str
    description: str
    handler: Callable[[dict[str, Any]], str]

    def run(self, args: dict[str, Any]) -> str:
        return self.handler(args)


def make_read_file_tool(root: Path | None = None) -> Tool:
    root = (root or Path(".")).resolve()

    def handler(args: dict[str, Any]) -> str:
        path = Path(args.get("path") or "")
        full = (root / path).resolve() if not path.is_absolute() else path.resolve()
        if root not in full.parents and full != root:
            return f"error: path escapes sandbox root ({root})"
        if not full.exists():
            return f"error: not found: {full}"
        return full.read_text(encoding="utf-8", errors="replace")[:8000]

    return Tool(
        name="read_file",
        description="Read a UTF-8 text file under the sandbox root. Args: {path}",
        handler=handler,
    )


def make_rag_tool(index: Index | Path) -> Tool:
    idx = load_index(index) if isinstance(index, Path) else index

    def handler(args: dict[str, Any]) -> str:
        q = str(args.get("query") or "")
        k = int(args.get("top_k") or 4)
        hits = retrieve(idx, q, top_k=k)
        return pack_citations(hits) or "no hits"

    return Tool(
        name="rag_search",
        description="Hybrid RAG search. Args: {query, top_k?}",
        handler=handler,
    )


def tools_catalog(tools: list[Tool]) -> str:
    return "\n".join(f"- {t.name}: {t.description}" for t in tools)
