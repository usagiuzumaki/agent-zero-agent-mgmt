"""Agent that evaluates commercial potential and audience appeal."""

from agents import AgentConfig, UserMessage
from .base import ScreenwritingAgent


class Marketability(ScreenwritingAgent):
    """Judge the market potential of a screenplay."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def assess(self, synopsis: str) -> str:
        """Return marketability analysis for the given synopsis.

        Uses tools and instruments to support its assessment.
        """
        msg = UserMessage(
            "Use available tools to evaluate marketability of:\n" +
            synopsis)
        self.hist_add_user_message(msg)
        return await self.monologue()

    async def analyze(self, text: str) -> str:
        """Standard interface for pipeline integration."""
        return await self.assess(text)
