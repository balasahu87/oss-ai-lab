from __future__ import annotations

import json
import re
from collections import Counter
from typing import Callable

from llmboost.client import LLMClient


def expand_queries(llm: LLMClient, question: str, n: int = 3) -> list[str]:
    """Ask the model for alternate search queries; always includes the original."""
    prompt = (
        f"Rewrite the user question into {n} diverse search queries, one per line, "
        f"no numbering.\n\nQuestion: {question}"
    )
    raw = llm.complete(prompt)
    alts = [ln.strip("-• \t") for ln in raw.splitlines() if ln.strip()]
    out = [question]
    for a in alts:
        if a and a.lower() != question.lower() and a not in out:
            out.append(a)
        if len(out) >= n + 1:
            break
    while len(out) < n + 1:
        out.append(f"{question} (variant {len(out)})")
    return out[: n + 1]


def self_consistency(
    llm: LLMClient,
    prompt: str,
    *,
    n: int = 3,
    normalize: Callable[[str], str] | None = None,
) -> str:
    """Sample n answers and majority-vote (offline-friendly with EchoClient)."""
    answers = [llm.complete(f"{prompt}\n\n(Reasoning path {i+1})") for i in range(n)]
    norm = normalize or (lambda s: re.sub(r"\s+", " ", s.strip().lower()))
    counts = Counter(norm(a) for a in answers)
    winner_norm, _ = counts.most_common(1)[0]
    for a in answers:
        if norm(a) == winner_norm:
            return a
    return answers[0]


def critique_revise(llm: LLMClient, question: str, draft: str, criteria: str = "") -> str:
    criteria = criteria or "correctness, grounding, clarity, and brevity"
    critique = llm.complete(
        f"Critique the draft answer against: {criteria}.\n"
        f"Question: {question}\nDraft:\n{draft}\n\nList issues briefly."
    )
    revised = llm.complete(
        f"Revise the draft using the critique. Return only the improved answer.\n"
        f"Question: {question}\nDraft:\n{draft}\nCritique:\n{critique}"
    )
    return revised.strip()


def repair_json(llm: LLMClient, broken: str, schema_hint: str = "") -> dict:
    """Attempt to parse JSON; on failure ask the LLM to repair."""
    try:
        return json.loads(broken)
    except json.JSONDecodeError:
        pass
    prompt = (
        "Fix the following into valid JSON only (no markdown).\n"
        f"Schema hint: {schema_hint or 'any object'}\n\n{broken}"
    )
    fixed = llm.complete(prompt).strip()
    fixed = re.sub(r"^```(?:json)?\s*|\s*```$", "", fixed, flags=re.I | re.M)
    return json.loads(fixed)
