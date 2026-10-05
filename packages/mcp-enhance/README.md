# mcp-enhance

TypeScript **MCP** servers that give any MCP host (Cursor, Claude Desktop, custom agents)
extra capabilities:

| Tool | Purpose |
|------|---------|
| `memory_set` / `memory_get` / `memory_list` | Persistent notes |
| `web_fetch` | Safe URL fetch + truncate |
| `structured_repair` | Prompt template to repair invalid JSON |
| `rag_retrieve` | Shells out to `ragline ask` when installed |

## Run

```bash
npm install
npm run build
node dist/index.js
```

## Cursor / Claude Desktop config

```json
{
  "mcpServers": {
    "oss-ai-enhance": {
      "command": "node",
      "args": ["/ABS/PATH/oss-ai-lab/packages/mcp-enhance/dist/index.js"]
    }
  }
}
```
