from python.helpers.tool import Tool, Response


class NarrativeKnowledge(Tool):
    """Provide structural insights based on genre and tone."""

    async def execute(self, query: str = "", genre: str = "", tone: str = "", **kwargs) -> Response:
        """Return narrative guidance for the given query."""
        message = f"Narrative insight for {genre} ({tone}): {query}"
        return Response(message=message, break_loop=False)
