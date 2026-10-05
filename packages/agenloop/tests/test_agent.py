from pathlib import Path

from agenloop import Agent, make_rag_tool
from ragline.index import build_index, save_index


class Scripted:
    def complete(self, prompt: str) -> str:
        if "OBS[" in prompt:
            return "FINAL: Hybrid retrieval combines BM25 and dense vectors via RRF."
        return '{"tool":"rag_search","args":{"query":"hybrid retrieval"}}'


def test_agent_uses_rag_and_finishes(tmp_path: Path):
    docs = Path(__file__).resolve().parents[3] / "sample_docs"
    idx = build_index(sorted(docs.glob("*.md")))
    save_index(idx, tmp_path / "idx")
    agent = Agent(llm=Scripted(), tools=[make_rag_tool(tmp_path / "idx")], max_steps=4)
    result = agent.run("Explain hybrid retrieval briefly.")
    assert result.steps == 2
    assert "hybrid" in result.answer.lower() or "bm25" in result.answer.lower()
