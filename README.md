# OSS AI Lab

**Agentic AI · RAG · Generative AI · MCP · LLM capability enhancement**

A showcase monorepo of production-minded open-source building blocks for
retrieval-augmented generation, tool-using agents, Model Context Protocol
servers, and techniques that stretch LLM reliability without vendor lock-in.

Built for interviews (OpenAI / Anthropic / AI labs) and as a seed for an
independent AI product company.

[![CI](https://github.com/balasahu87/oss-ai-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/balasahu87/oss-ai-lab/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## Packages

| Package | Stack | What it does |
|---------|-------|----------------|
| [`ragline`](packages/ragline) | Python | Hybrid RAG (BM25 + dense vectors), citations, CLI |
| [`llmboost`](packages/llmboost) | Python | Multi-query, self-consistency, critique-revise, JSON repair |
| [`agenloop`](packages/agenloop) | Python | Plan → tool → observe → reflect agent runtime |
| [`mcp-enhance`](packages/mcp-enhance) | TypeScript | MCP servers: memory, web-fetch, structured-repair, rag-retrieve |

```text
User / IDE
   │
   ├─ MCP (mcp-enhance) ── tools over stdio
   │
   └─ Agent (agenloop)
         ├─ llmboost  (reasoning enhancers)
         └─ ragline   (grounded retrieval)
```

## Quick start (offline demos — no API key)

```bash
cd oss-ai-lab

# Python packages (editable)
python3 -m venv .venv && source .venv/bin/activate
pip install -e packages/ragline -e packages/llmboost -e packages/agenloop
pip install pytest

# Index sample docs + ask
ragline index sample_docs --out .ragline_index
ragline ask "What is hybrid retrieval?" --index .ragline_index

# Agent loop with mock LLM (offline)
python demos/demo_agent_offline.py

# MCP (Node 18+)
cd packages/mcp-enhance && npm install && npm run build
node dist/index.js --help
```

## With an OpenAI-compatible API

```bash
cp .env.example .env   # set OPENAI_API_KEY / OPENAI_API_BASE / OPENAI_MODEL
python demos/demo_agent_online.py
```

## Why this exists

Most “AI demos” hide retrieval quality, tool budgets, and failure modes.
OSS AI Lab makes those choices explicit:

- **Grounding** — hybrid retrieval + citation packing (`ragline`)
- **Reliability** — self-consistency / critique loops (`llmboost`)
- **Agency** — bounded tool loops with memory (`agenloop`)
- **Interop** — MCP servers any IDE/agent can call (`mcp-enhance`)

## Interview talking points

See [docs/INTERVIEW.md](docs/INTERVIEW.md) for architecture trade-offs,
eval ideas, and how to walk interviewers through the code in 10 minutes.

## License

MIT — see [LICENSE](LICENSE).
