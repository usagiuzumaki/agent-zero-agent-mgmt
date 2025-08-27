"""Agent that collaborates on drafting and editing scenes."""

from agents import AgentConfig
from .base import ScreenwritingAgent


class CoWriter(ScreenwritingAgent):
    """Assist in writing or rewriting screenplay content."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def draft(self, prompt: str) -> str:
        """Generate or revise scenes based on the prompt.

        Utilizes tools and instruments to enhance creative output.
        """
        self.hist_add_user_message(
            "Use available tools to collaborate on the following request:\n" + prompt
        )
        return await self.monologue()
