from python.helpers.tool import Tool, Response
from agents import Agent

class InjectFourthWallBreak(Tool):
    """
    Inject a meta-humorous fourth wall break into the scene.
    """
    def __init__(self, agent: Agent, name="inject_fourth_wall_break", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        character = self.args.get("character", kwargs.get("character"))
        target_line = self.args.get("target_line", kwargs.get("target_line", ""))
        meta_commentary = self.args.get("meta_commentary", kwargs.get("meta_commentary"))
        return Response(message=f"[{character} turns to the camera during '{target_line}']: {meta_commentary}", break_loop=False)
