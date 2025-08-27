"""Agent that formats a script into shareable HTML."""

from agents import AgentConfig
from .base import ScreenwritingAgent


class ScriptFormatter(ScreenwritingAgent):
    """Produce formatted HTML from a Fountain script."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def format(self, script: str) -> str:
        """Return HTML representation using the fountain_to_html instrument."""
        self.hist_add_user_message(
            "Use the fountain_to_html instrument to render this script:\n" + script
        )
        return await self.monologue()
