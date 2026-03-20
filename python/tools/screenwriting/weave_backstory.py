from python.helpers.tool import Tool, Response
from agents import Agent

class WeaveBackstory(Tool):
    """
    Weave a character's backstory into the current scene.
    """
    def __init__(self, agent: Agent, name="weave_backstory", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        character = self.args.get("character", kwargs.get("character"))
        backstory = self.args.get("backstory_element", kwargs.get("backstory_element"))

        return Response(message=f"BACKSTORY WEAVED for {character}: {backstory}", break_loop=False)
