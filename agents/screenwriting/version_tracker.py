"""Agent that tracks revisions and manages screenplay versions."""

from agents import AgentConfig
from .base import ScreenwritingAgent


class VersionTracker(ScreenwritingAgent):
    """Keep history of script versions and changes."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    async def record(self, note: str) -> str:
        """Log a version note for the screenplay.

        Relies on tools and instruments to persist information.
        """
        self.hist_add_user_message(
            "Use tools and instruments to track this revision note:\n" + note
        )
        return await self.monologue()
