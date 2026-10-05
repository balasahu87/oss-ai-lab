# Agentic Loops

An agentic loop is: **plan → select tool → execute → observe → reflect**.
Without budgets (max steps, max tokens, tool allowlists) agents can loop
forever or call unsafe tools. Short-term scratchpad memory stores
intermediate observations; long-term memory should be explicit and curated.

## Tool use

Tools should return structured observations, not free-form prose only.
The model then decides whether to call another tool or produce a final answer.
MCP (Model Context Protocol) standardizes how IDEs and hosts expose tools.
