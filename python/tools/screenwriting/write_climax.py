from python.helpers.tool import Tool, Response
from agents import Agent

class WriteClimax(Tool):
    """
    Write the climax of a scene or act.
    """
    def __init__(self, agent: Agent, name="write_climax", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        build_up = self.args.get("build_up", kwargs.get("build_up", ""))
        climax = self.args.get("climax_event", kwargs.get("climax_event"))

        return Response(message=f"CLIMAX:\nBuild-up: {build_up}\nEvent: {climax}", break_loop=False)
