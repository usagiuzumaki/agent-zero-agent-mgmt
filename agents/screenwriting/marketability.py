"""Agent that evaluates commercial potential and audience appeal."""

from agents import AgentConfig
from .base import ScreenwritingAgent


class Marketability(ScreenwritingAgent):
    """Judge the market potential of a screenplay."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def assess(self, synopsis: str) -> str:
        """Return marketability analysis for the given synopsis.

        Uses tools and instruments to support its assessment.
        """
        self.hist_add_user_message(
            "Use available tools to evaluate marketability of:\n" + synopsis
        )
        return await self.monologue()
