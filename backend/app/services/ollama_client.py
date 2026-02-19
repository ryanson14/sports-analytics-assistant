"""
Ollama client - talks to a local Ollama API for LLM responses.
Placeholder for implementation.
"""
from typing import Any


class OllamaClient:
    """Client for the Ollama HTTP API (e.g. llama3, mistral)."""

    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3") -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def generate(self, prompt: str, **kwargs: Any) -> str:
        """
        Send prompt to Ollama and return the generated text.
        Placeholder.
        """
        # TODO: POST to /api/generate, stream or wait for full response
        return ""

    def chat(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        """
        Send a list of messages (e.g. [{"role": "user", "content": "..."}]) and return the reply.
        Placeholder.
        """
        # TODO: POST to /api/chat
        return ""
