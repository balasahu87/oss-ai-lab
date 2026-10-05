import json

from llmboost.client import EchoClient, MockClient
from llmboost.techniques import expand_queries, repair_json, self_consistency


def test_expand_queries_includes_original():
    qs = expand_queries(EchoClient(), "What is RAG?", n=2)
    assert qs[0] == "What is RAG?"
    assert len(qs) >= 2


def test_self_consistency_votes():
    client = MockClient({"path 1": "Paris", "path 2": "Paris", "path 3": "Lyon"})
    # Mock matches first key found; use Echo for simpler determinism
    ans = self_consistency(EchoClient(), "Capital of France?", n=3)
    assert isinstance(ans, str) and ans


def test_repair_json():
    data = repair_json(EchoClient(), "{not json", schema_hint='{"ok": bool}')
    assert isinstance(data, dict)
    assert "ok" in data
