from python.helpers.tool import Tool, Response


class StoryStructure(Tool):
    """Validate plot progression using beat sheets."""

    async def execute(
        self,
        act: str = "",
        beat: str = "",
        tension_level: str = "",
        **kwargs,
    ) -> Response:
        """Return a simple structure check message."""
        message = (
            f"Structure check - Act {act}, Beat {beat}, Tension {tension_level}"
        )
        return Response(message=message, break_loop=False)
