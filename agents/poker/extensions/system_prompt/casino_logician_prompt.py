from typing import Any
from python.helpers.extension import Extension
from agents import Agent, LoopData

class CasinoLogicianPrompt(Extension):
    """
    Extension to inject the Casino Logician persona when the poker profile is active.
    """
    async def execute(self, system_prompt: list[str] = [], loop_data: LoopData = LoopData(), **kwargs: Any):
        # The agent.read_prompt will look into agents/poker/prompts/ because the profile is set to 'poker'
        logician_prompt = self.agent.read_prompt("casino_logician.system.md")
        if logician_prompt:
            system_prompt.append(logician_prompt)
