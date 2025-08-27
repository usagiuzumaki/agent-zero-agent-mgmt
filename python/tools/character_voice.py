from python.helpers.tool import Tool, Response


class CharacterVoice(Tool):
    """Generate dialogue in a character's voice."""

    async def execute(
        self,
        character: str = "",
        emotional_state: str = "",
        scene_context: str = "",
        **kwargs,
    ) -> Response:
        """Return a short dialogue sample for the character."""
        message = (
            f"Dialogue sample for {character} "
            f"[{emotional_state}] in {scene_context}"
        )
        return Response(message=message, break_loop=False)
