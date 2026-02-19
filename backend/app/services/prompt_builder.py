"""
Prompt builder - constructs prompts for the LLM using context (StatMuse, metrics, etc.).
Placeholder for implementation.
"""
from typing import Any


class PromptBuilder:
    """Build structured prompts for the sports analytics assistant."""

    def __init__(self, system_prompt: str | None = None) -> None:
        self.system_prompt = system_prompt or "You are a sports analytics assistant."

    def build(
        self,
        user_query: str,
        statmuse_context: list[dict[str, Any]] | None = None,
        fantasy_context: dict[str, Any] | None = None,
    ) -> str:
        """
        Build a full prompt from user query and optional context.
        Placeholder.
        """
        # TODO: combine system_prompt, user_query, statmuse_context, fantasy_context
        return f"{self.system_prompt}\n\nUser: {user_query}"

    def build_system_with_context(self, context: dict[str, Any]) -> str:
        """Build or update system prompt with injected context. Placeholder."""
        # TODO: inject stats/context into system prompt
        return self.system_prompt
