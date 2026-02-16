from python.helpers.tool import Tool, Response


class FormatVerify(Tool):

    async def execute(
        self, scene_type: str = "", formatting_standard: str = "", **kwargs
    ) -> Response:

        message = (
            f"Format check for {scene_type} using {formatting_standard} standard"
        )
        return Response(message=message, break_loop=False)
