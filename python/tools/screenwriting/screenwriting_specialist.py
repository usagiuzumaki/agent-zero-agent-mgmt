from python.helpers.tool import Tool, Response
from agents import Agent

class ScreenwritingSpecialist(Tool):
    """
    Smart router for screenwriting tools.
    """
    def __init__(self, agent: Agent, name="screenwriting_specialist", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        mode = self.args.get("mode", kwargs.get("mode", "pipeline"))
        prompt = self.args.get("prompt", kwargs.get("prompt", ""))

        if not prompt:
            return Response(message="Error: prompt is required.", break_loop=False)

        if mode == "pipeline":
             pipeline = self.agent.get_tool(
                 name="screenwriting_pipeline",
                 method=None,
                 args={"prompt": prompt},
                 message=prompt,
                 loop_data=None
             )
             return await pipeline.execute(prompt=prompt)

        elif mode == "direct":
             tool_name = self.args.get("tool_name", kwargs.get("tool_name", ""))
             if not tool_name:
                 return Response(message="Error: tool_name required in direct mode.", break_loop=False)

             # Convert CamelCase to snake_case if necessary
             import re
             tool_snake_name = re.sub(r'(?<!^)(?=[A-Z])', '_', tool_name).lower()

             tool_instance = self.agent.get_tool(
                 name=tool_snake_name,
                 method=None,
                 args={"context": prompt},
                 message=prompt,
                 loop_data=None
             )

             if not tool_instance or tool_instance.__class__.__name__ == 'Unknown':
                 return Response(message=f"Error: Tool '{tool_name}' not found.", break_loop=False)

             return await tool_instance.execute(context=prompt)

        else:
             return Response(message=f"Error: Unknown mode '{mode}'.", break_loop=False)
