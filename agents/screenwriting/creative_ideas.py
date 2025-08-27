"""Agent that proposes plot twists, themes and creative concepts."""

from agents import AgentConfig
from .base import ScreenwritingAgent


class CreativeIdeas(ScreenwritingAgent):
    """Generate creative ideas for screenwriting projects."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def brainstorm(self, topic: str) -> str:
        """Produce ideas or twists related to the topic.

        May use external instruments to broaden its suggestions.
        """
        self.hist_add_user_message(
            "Use tools and instruments to brainstorm around:\n" + topic
        )
        return await self.monologue()
