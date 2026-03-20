from python.helpers.tool import Tool, Response
from agents import Agent

class EscalateTension(Tool):
    """
    Escalate the dramatic tension in preparation for the climax.
    """
    def __init__(self, agent: Agent, name="escalate_tension", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        stakes = self.args.get("current_stakes", kwargs.get("current_stakes", "Low"))
        new_stakes = self.args.get("new_stakes", kwargs.get("new_stakes"))
        turning = self.args.get("turning_point", kwargs.get("turning_point"))

        output = f"TENSION ESCALATED from {stakes} to {new_stakes} at {turning}."
        return Response(message=output, break_loop=False)
