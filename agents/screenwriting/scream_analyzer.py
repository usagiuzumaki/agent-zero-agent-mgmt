"""Agent that detects and analyzes intense emotional outbursts."""

from agents import AgentConfig
from .base import ScreenwritingAgent


class ScreamAnalyzer(ScreenwritingAgent):
    """Identify moments of heightened emotion or screams within text."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def analyze(self, text: str) -> str:
        """Use tools to highlight screams or similar exclamations in the text."""
        self.hist_add_user_message(
            "Use available tools to analyze the following text for screams or intense emotional outbursts:\n" + text
        )
        return await self.monologue()
