"""Agent that produces a simple visual storyboard outline."""

from agents import AgentConfig
from .base import ScreenwritingAgent


class StoryboardGenerator(ScreenwritingAgent):
    """Generate scene-by-scene visual prompts for artists."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def generate(self, script: str) -> str:
        """Use tools to craft a visual storyboard from script text."""
        self.hist_add_user_message(
            "Create a concise visual storyboard for the following script:\n" + script
        )
        return await self.monologue()
