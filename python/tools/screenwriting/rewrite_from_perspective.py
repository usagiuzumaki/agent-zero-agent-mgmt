from python.helpers.tool import Tool, Response
from agents import Agent

class RewriteFromPerspective(Tool):
    """
    Rewrite a scene from an entirely different, unexpected character's point of view.
    """
    def __init__(self, agent: Agent, name="rewrite_from_perspective", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        char = self.args.get("new_perspective_character", kwargs.get("new_perspective_character", ""))
        rewrite = self.args.get("rewritten_scene", kwargs.get("rewritten_scene", ""))

        output = f"PERSPECTIVE SHIFT ({char}):\n{rewrite}"
        return Response(message=output, break_loop=False)
