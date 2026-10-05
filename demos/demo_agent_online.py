#!/usr/bin/env python3
"""Online agent demo — requires OPENAI_API_KEY (OpenAI-compatible)."""
from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [
    str(ROOT / "packages" / "ragline" / "src"),
    str(ROOT / "packages" / "llmboost" / "src"),
    str(ROOT / "packages" / "agenloop" / "src"),
]

from agenloop import Agent, make_rag_tool, make_read_file_tool
from llmboost import OpenAICompatClient
from ragline.index import build_index, save_index


def main() -> None:
    if not os.getenv("OPENAI_API_KEY"):
        raise SystemExit("Set OPENAI_API_KEY (see .env.example)")
    docs = ROOT / "sample_docs"
    out = ROOT / ".ragline_index"
    idx = build_index(sorted(docs.glob("*.md")))
    save_index(idx, out)
    llm = OpenAICompatClient()
    agent = Agent(
        llm=llm,
        tools=[make_rag_tool(out), make_read_file_tool(ROOT / "sample_docs")],
        max_steps=6,
    )
    result = agent.run(
        "Using tools, explain how MCP relates to agentic tool use in 3 bullets."
    )
    print(result.answer)
    print("--- steps:", result.steps)


if __name__ == "__main__":
    main()
