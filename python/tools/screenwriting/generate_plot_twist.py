from python.helpers.tool import Tool, Response
from agents import Agent

class GeneratePlotTwist(Tool):
    """
    Generate an unpredictable plot twist.
    """
    def __init__(self, agent: Agent, name="generate_plot_twist", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        scenario = self.args.get("current_scenario", kwargs.get("current_scenario", ""))
        twist_type = self.args.get("twist_type", kwargs.get("twist_type", "Unexpected"))
        twist = self.args.get("twist_description", kwargs.get("twist_description", ""))

        output = f"PLOT TWIST ({twist_type}):\n{twist}\n\nImpacts scenario: {scenario}"
        return Response(message=output, break_loop=False)
