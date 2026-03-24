from python.helpers.tool import Tool, Response
from agents import Agent

class FormatActionSequence(Tool):
    """
    Format a high-octane action sequence to improve pacing.
    """
    def __init__(self, agent: Agent, name="format_action_sequence", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        characters = self.args.get("characters_involved", kwargs.get("characters_involved", []))
        beats = self.args.get("action_beats", kwargs.get("action_beats", []))
        pacing = self.args.get("pacing_notes", kwargs.get("pacing_notes", ""))

        output = f"ACTION SEQUENCE with {', '.join(characters)}:\n"
        for beat in beats:
            output += f"- {beat}\n"
        output += f"Pacing: {pacing}"
        return Response(message=output, break_loop=False)
