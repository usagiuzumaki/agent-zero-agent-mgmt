"""Agent for checking world-building consistency."""

from agents import AgentConfig
from .base import ScreenwritingAgent


class WorldBuilder(ScreenwritingAgent):
    """Examine lore notes for continuity and logical coherence."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def build(self, bible: str) -> str:
        """Use tools to verify world-building consistency."""
        self.hist_add_user_message(
            "Review the following world-building bible for consistency and contradictions:\n" + bible
        )
        return await self.monologue()
