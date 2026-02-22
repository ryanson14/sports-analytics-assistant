"""
Send prompts to a local Ollama instance at localhost:11434 and return the response.
"""
from typing import Any

import httpx

DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "llama3.1:8b"


async def ask_ollama(
    prompt: str,
    *,
    base_url: str = DEFAULT_BASE_URL,
    model: str = DEFAULT_MODEL,
    stream: bool = False,
) -> str:
    """
    POST prompt to Ollama /api/generate and return the generated text.
    Uses stream=False by default to get a single response body.
    """
    url = f"{base_url.rstrip('/')}/api/generate"
    payload: dict[str, Any] = {
        "model": model,
        "prompt": prompt,
        "stream": stream,
    }

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()

    return (data.get("response") or "").strip()
