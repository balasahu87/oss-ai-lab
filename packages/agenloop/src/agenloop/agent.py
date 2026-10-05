from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from llmboost.client import LLMClient

from agenloop.memory import Scratchpad
from agenloop.tools import Tool, tools_catalog


@dataclass
class AgentResult:
    answer: str
    steps: int
    trace: list[str] = field(default_factory=list)


_TOOL_RE = re.compile(r"\{[^{}]*\"tool\"[^{}]*\}", re.S)


class Agent:
    """
    Simple ReAct-style loop.
    The model must either:
      {"tool": "name", "args": {...}}
    or:
      FINAL: <answer>
    """

    def __init__(
        self,
        llm: LLMClient,
        tools: list[Tool],
        *,
        max_steps: int = 6,
        system: str = "",
    ):
        self.llm = llm
        self.tools = {t.name: t for t in tools}
        self.max_steps = max_steps
        self.system = system or (
            "You are a careful tool-using agent. Prefer tools for factual lookups. "
            "When done, reply with FINAL: followed by the answer."
        )
        self.memory = Scratchpad()

    def run(self, goal: str) -> AgentResult:
        trace: list[str] = []
        self.memory.add(f"GOAL: {goal}")
        for step in range(1, self.max_steps + 1):
            prompt = self._prompt(goal)
            raw = self.llm.complete(prompt)
            trace.append(f"step{step}: {raw[:400]}")
            self.memory.add(f"THOUGHT: {raw[:1000]}")

            if "FINAL:" in raw:
                answer = raw.split("FINAL:", 1)[1].strip()
                return AgentResult(answer=answer, steps=step, trace=trace)

            call = self._parse_tool(raw)
            if not call:
                # force finish
                answer = self.llm.complete(
                    f"{prompt}\n\nModel output was not a tool call. "
                    f"Provide FINAL: answer now based on scratchpad.\n{self.memory.dump()}"
                )
                if "FINAL:" in answer:
                    answer = answer.split("FINAL:", 1)[1].strip()
                return AgentResult(answer=answer.strip(), steps=step, trace=trace)

            name = call.get("tool")
            args = call.get("args") or {}
            tool = self.tools.get(str(name))
            if not tool:
                obs = f"error: unknown tool {name}"
            else:
                obs = tool.run(args if isinstance(args, dict) else {})
            self.memory.add(f"OBS[{name}]: {obs[:2000]}")
            trace.append(f"obs[{name}]: {obs[:200]}")

        return AgentResult(
            answer="Reached max_steps without FINAL.",
            steps=self.max_steps,
            trace=trace,
        )

    def _prompt(self, goal: str) -> str:
        return (
            f"{self.system}\n\nTools:\n{tools_catalog(list(self.tools.values()))}\n\n"
            f"Scratchpad:\n{self.memory.dump()}\n\n"
            f"Goal: {goal}\n"
            'Respond with either {"tool":"...","args":{...}} or FINAL: ...'
        )

    def _parse_tool(self, raw: str) -> dict[str, Any] | None:
        raw = raw.strip()
        try:
            data = json.loads(raw)
            if isinstance(data, dict) and "tool" in data:
                return data
        except json.JSONDecodeError:
            pass
        m = _TOOL_RE.search(raw)
        if not m:
            return None
        try:
            data = json.loads(m.group(0))
            if isinstance(data, dict) and "tool" in data:
                return data
        except json.JSONDecodeError:
            return None
        return None
