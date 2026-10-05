# LLM Capability Enhancement

Techniques that improve answer quality without fine-tuning:

1. **Multi-query expansion** — rewrite the user question several ways, retrieve for each, merge.
2. **Self-consistency** — sample multiple reasoning paths, majority-vote the answer.
3. **Critique-revise** — draft, critique against criteria, revise once.
4. **Structured repair** — if JSON/schema validation fails, ask the model to fix errors only.

These are orthogonal to model size: they trade latency/cost for reliability.
