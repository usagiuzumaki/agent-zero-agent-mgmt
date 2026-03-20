from python.helpers.tool import Tool, Response
from agents import Agent

class GenerateCharacterMotivation(Tool):
    """
    Generate deep psychological and mystical motivation for a character's actions.
    """
    def __init__(self, agent: Agent, name="generate_character_motivation", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        character = self.args.get("character", kwargs.get("character"))
        action = self.args.get("action", kwargs.get("action"))
        tarot = self.args.get("tarot_archetype", kwargs.get("tarot_archetype", "The Fool"))
        hidden = self.args.get("hidden_motivation", kwargs.get("hidden_motivation"))

        output = f"MOTIVATION for {character} doing {action}:\n"
        output += f"Tarot: {tarot}\n"
        output += f"Hidden Truth: {hidden}"
        return Response(message=output, break_loop=False)
