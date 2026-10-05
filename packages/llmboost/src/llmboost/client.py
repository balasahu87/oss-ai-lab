from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Protocol


class LLMClient(Protocol):
    def complete(self, prompt: str) -> str: ...


class EchoClient:
    """Offline stub: returns a deterministic transform of the prompt."""

    def complete(self, prompt: str) -> str:
        lines = [ln.strip() for ln in prompt.strip().splitlines() if ln.strip()]
        tail = lines[-1] if lines else prompt
        if "JSON" in prompt or "json" in prompt:
            return '{"ok": true, "note": "echo"}'
        return f"[echo] {tail[:500]}"


class MockClient:
    """Map substrings → canned answers for demos/tests."""

    def __init__(self, mapping: dict[str, str] | None = None):
        self.mapping = mapping or {}

    def complete(self, prompt: str) -> str:
        for key, val in self.mapping.items():
            if key.lower() in prompt.lower():
                return val
        return "I don't know (mock)."


class OpenAICompatClient:
    """Minimal Chat Completions client (OpenAI / Azure / local gateways)."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
    ):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or ""
        self.base_url = (base_url or os.getenv("OPENAI_API_BASE") or "https://api.openai.com/v1").rstrip(
            "/"
        )
        self.model = model or os.getenv("OPENAI_MODEL") or "gpt-4o-mini"

    def complete(self, prompt: str) -> str:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY not set")
        url = f"{self.base_url}/chat/completions"
        body = json.dumps(
            {
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.2,
            }
        ).encode()
        req = urllib.request.Request(
            url,
            data=body,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"LLM HTTP {e.code}: {e.read()[:500]!r}") from e
        return data["choices"][0]["message"]["content"]
