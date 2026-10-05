# Architecture

## ragline

1. Chunk markdown/text with overlap.
2. Build BM25 index over tokens.
3. Embed chunks with a deterministic hashing embedder (offline) or pluggable model.
4. Query: BM25 top-k + dense top-k → RRF → citation pack.

## llmboost

Pure functions around an `LLMClient` protocol (`complete(prompt) -> str`).
Offline demos use `EchoClient` / `MockClient`.

## agenloop

`Agent` holds tools, memory, and a step budget. Each turn the LLM returns
either a final answer or a tool call JSON. Observations append to the
scratchpad.

## mcp-enhance

TypeScript MCP server (stdio) registering tools. `rag-retrieve` shells out
to `ragline` CLI when available; otherwise returns a helpful error.
