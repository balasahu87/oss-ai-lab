# agenloop

Bounded **agentic loop**: plan → tool call → observe → reflect.

```python
from agenloop import Agent, Tool
from llmboost import EchoClient

agent = Agent(llm=EchoClient(), tools=[...], max_steps=5)
print(agent.run("Summarize hybrid retrieval from the index"))
```
