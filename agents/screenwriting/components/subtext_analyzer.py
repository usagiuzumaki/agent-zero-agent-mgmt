"""Agent that identifies hidden meanings and unsaid motivations in scripts."""

from agents import AgentConfig, UserMessage
from .base import ScreenwritingAgent


class SubtextAnalyzer(ScreenwritingAgent):
    """Analyze script for subtext, unsaid emotions, and on-the-nose dialogue."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def analyze(self, script: str) -> str:
        """Deep dive into the subtext of the provided script fragment.

        Uses the Subtext Whisperer persona for sophisticated analysis.
        """
        # Load the specialized system prompt for subtext analysis
        subtext_prompt = self.read_prompt("mythic/subtext_whisperer.system.md")

        msg = UserMessage(
            message="Analyze the subtext of the following script. Be deep and insightful:\n\n" + script,
            system_message=[subtext_prompt]
        )
        self.hist_add_user_message(msg)
        return await self.monologue()
