"""Agent that tracks and amplifies emotional stakes in scripts."""

from agents import AgentConfig, UserMessage
from .base import ScreenwritingAgent


class EmotionalTension(ScreenwritingAgent):
    """Analyze emotional pacing and suggest tension improvements."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def analyze(self, script: str) -> str:
        """Assess emotional tension across the script.

        Employs tools and instruments to map intensity levels.
        """
        msg = UserMessage(
            message="Use tools and instruments to assess emotional tension in:\n" + script
        )
        self.hist_add_user_message(msg)
        return await self.monologue()

    async def gauge(self, script: str) -> str:
        """Alias for analyze."""
        return await self.analyze(script)
