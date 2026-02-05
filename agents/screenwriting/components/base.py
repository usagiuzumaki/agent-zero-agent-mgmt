"""Common base for screenwriting agents with integrated help manual."""

from agents import Agent, AgentConfig
from python.helpers import files


class ScreenwritingAgent(Agent):
    """Screenwriting agent base that can display editing help instructions."""

    def __init__(self, number: int, config: AgentConfig, context=None):
        super().__init__(number, config, context)

    def help(self) -> str:
        """Return the screenwriting manual with available editing commands."""
        path = files.get_abs_path("agents", "screenwriting", "prompts", "help.md")
        return files.read_file(path)
