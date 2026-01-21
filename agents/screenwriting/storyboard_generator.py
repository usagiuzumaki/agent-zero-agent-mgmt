"""Agent that produces a simple visual storyboard outline."""

from agents import AgentConfig, UserMessage
from .base import ScreenwritingAgent


class StoryboardGenerator(ScreenwritingAgent):
    """Generate scene-by-scene visual prompts for artists."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def generate(self, script: str) -> str:
        """Use tools to craft a visual storyboard from script text."""
        self.hist_add_user_message(
            UserMessage("Create a concise visual storyboard for the following script:\n" + script)
        )
        self.hist_add_user_message(msg)
        return await self.monologue()

    async def analyze(self, text: str) -> str:
        """Standard interface for pipeline integration."""
        return await self.generate(text)
    async def analyze(self, script: str) -> str:
        """Alias for generate."""
        return await self.generate(script)
