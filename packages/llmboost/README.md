# llmboost

Techniques that enhance LLM reliability without fine-tuning:

- Multi-query expansion
- Self-consistency (majority vote)
- Critique → revise
- Structured JSON repair

Works with any client implementing `complete(prompt: str) -> str`.
