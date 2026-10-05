#!/usr/bin/env python3
"""Offline agent demo — no API key required."""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [
    str(ROOT / "packages" / "ragline" / "src"),
    str(ROOT / "packages" / "llmboost" / "src"),
    str(ROOT / "packages" / "agenloop" / "src"),
]

from agenloop import Agent, make_rag_tool
from ragline.index import build_index, save_index


class ScriptedClient:
    """Return tool call once, then FINAL after observations appear."""

    def complete(self, prompt: str) -> str:
        if "OBS[" in prompt:
            return (
                "FINAL: Hybrid retrieval merges BM25 (sparse) and dense vector search "
                "with Reciprocal Rank Fusion for better RAG grounding."
            )
        return '{"tool":"rag_search","args":{"query":"hybrid retrieval RRF"}}'


def main() -> None:
    docs = ROOT / "sample_docs"
    out = ROOT / ".ragline_index"
    idx = build_index(sorted(docs.glob("*.md")))
    save_index(idx, out)
    print(f"indexed {len(idx.chunks)} chunks → {out}")

    agent = Agent(llm=ScriptedClient(), tools=[make_rag_tool(out)], max_steps=4)
    result = agent.run("In one sentence, what is hybrid retrieval?")
    print("steps:", result.steps)
    print("answer:", result.answer)
    print("trace:")
    for t in result.trace:
        print(" ", t[:160])


if __name__ == "__main__":
    main()
