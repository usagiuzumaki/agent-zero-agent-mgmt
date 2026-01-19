"""Agent that detects and analyzes intense emotional outbursts."""

from typing import Literal

from agents import AgentConfig, UserMessage
from .base import ScreenwritingAgent


Intensity = Literal["none", "low", "medium", "high"]


class ScreamAnalyzer(ScreenwritingAgent):
    """Identify and classify moments of heightened emotion or screams."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    @staticmethod
    def classify_intensity(text: str) -> Intensity:
        """Classify intensity based on exclamation marks and all-caps words."""
        exclamations = text.count("!")
        caps = sum(1 for w in text.split() if w.isupper() and len(w) > 1)
        score = exclamations + caps
        if score > 5:
            return "high"
        if score > 2:
            return "medium"
        if score > 0:
            return "low"
        return "none"

    async def analyze(self, text: str) -> str:
        """Highlight screams and return an intensity classification."""
        intensity = self.classify_intensity(text)
        self.hist_add_user_message(
            UserMessage(
                "Use available tools to analyze the following text for screams or intense emotional outbursts:\n"
                + text
            )
        )
        details = await self.monologue()
        return f"Intensity: {intensity}\n\n{details}"
