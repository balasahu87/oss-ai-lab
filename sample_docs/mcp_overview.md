# MCP — Model Context Protocol

MCP lets hosts (Cursor, Claude Desktop, custom agents) discover and call
tools over a standard transport (stdio or HTTP). Servers advertise tools
with JSON Schema inputs. This monorepo's `mcp-enhance` package ships
memory, web-fetch, structured-repair, and rag-retrieve tools so any MCP
client can gain RAG and persistence without baking them into the model.
