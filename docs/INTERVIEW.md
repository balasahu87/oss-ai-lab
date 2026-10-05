# Interview talking points (10 minutes)

## Pitch (30s)

> I open-sourced a monorepo that shows how I think about production LLM systems:
> hybrid RAG for grounding, an agent loop with budgets, MCP for tool interop,
> and capability enhancers (self-consistency, critique) that work with any
> OpenAI-compatible API — including offline demos for CI.

## Walk the code

1. **Retrieval quality** — `packages/ragline/src/ragline/retrieve.py` (RRF).
2. **Agent safety** — `packages/agenloop/src/agenloop/agent.py` (max_steps).
3. **Enhancers** — `packages/llmboost/src/llmboost/techniques.py`.
4. **Interop** — `packages/mcp-enhance/src/server.ts` (MCP tools).

## Trade-offs to mention

- Hashing embeddings ≠ SOTA quality; they make demos/CI deterministic.
- Self-consistency multiplies cost; use for high-stakes answers only.
- MCP stdio is great for IDEs; remote HTTP needs auth.

## Eval ideas (extension)

- Golden Q&A on `sample_docs/` with recall@k and citation overlap.
- Agent task success rate with fixed tool mocks.
- Schema repair success rate on broken JSON fixtures.
