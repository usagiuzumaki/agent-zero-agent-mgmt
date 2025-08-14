"""Agent that inspects plot structure and pacing."""

from agents import Agent, AgentConfig


class PlotAnalyzer(Agent):
    """Examine plot coherence and structural elements."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def analyze(self, outline: str) -> str:
        """Return a structural analysis of the provided outline.

        Makes use of tools and instruments for deeper inspection.
        """
        self.hist_add_user_message(
            "Use tools and instruments to analyze the plot structure of:\n" + outline
        )
        return await self.monologue()
