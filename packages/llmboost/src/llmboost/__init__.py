"""llmboost — capability enhancers for LLMs."""

from llmboost.client import EchoClient, LLMClient, MockClient, OpenAICompatClient
from llmboost.techniques import (
    critique_revise,
    expand_queries,
    repair_json,
    self_consistency,
)

__all__ = [
    "LLMClient",
    "EchoClient",
    "MockClient",
    "OpenAICompatClient",
    "expand_queries",
    "self_consistency",
    "critique_revise",
    "repair_json",
]
__version__ = "0.1.0"
