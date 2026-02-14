"""Agent for checking world-building consistency."""

from agents import AgentConfig, UserMessage
from .base import ScreenwritingAgent


class WorldBuilder(ScreenwritingAgent):
    """Examine lore notes for continuity and logical coherence."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def build(self, bible: str) -> str:
        """Use tools to verify world-building consistency."""
        msg = UserMessage(
            message="Review the following world-building bible for consistency and contradictions:\n" + bible
        )
        self.hist_add_user_message(msg)
        return await self.monologue()

    async def check(self, bible: str) -> str:
        """Alias for build."""
        return await self.build(bible)
