"""Agent that reviews and improves dialogue for natural flow."""

from agents import Agent, AgentConfig


class DialogueEvaluator(Agent):
    """Assess dialogue quality and suggest enhancements."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def evaluate(self, dialogue: str) -> str:
        """Return evaluation and improvements for the dialogue.

        Leverages tools and instruments to refine suggestions.
        """
        self.hist_add_user_message(
            "Use available tools to critique this dialogue:\n" + dialogue
        )
        return await self.monologue()
