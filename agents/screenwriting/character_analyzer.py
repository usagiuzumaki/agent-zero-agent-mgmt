"""Agent that evaluates character development and consistency."""

from agents import Agent, AgentConfig


class CharacterAnalyzer(Agent):
    """Analyze character arcs and traits within a script."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def analyze(self, script: str) -> str:
        """Return analysis of characters in the provided script.

        The agent may invoke tools and instruments to support its reasoning.
        """
        self.hist_add_user_message(
            "Use tools like the script_analyzer instrument to analyze the characters in the following script:\n"
            + script
        )
        return await self.monologue()
