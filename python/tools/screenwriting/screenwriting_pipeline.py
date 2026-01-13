from agents import Agent, UserMessage
from python.helpers.tool import Tool, Response
from agents.screenwriting.plot_analyzer import PlotAnalyzer
from agents.screenwriting.creative_ideas import CreativeIdeas
from agents.screenwriting.co_writer import CoWriter
from agents.screenwriting.dialogue_evaluator import DialogueEvaluator
from agents.screenwriting.script_formatter import ScriptFormatter
import json
from python.helpers.print_style import PrintStyle

class ScreenwritingPipeline(Tool):
    """
    Orchestrates a screenwriting pipeline by handing off tasks to specialized agents.
    Each agent handles a specific writing tool process:
    1. PlotAnalyzer (Structure)
    2. CreativeIdeas (Brainstorming)
    3. CoWriter (Drafting)
    4. DialogueEvaluator (Refinement)
    5. ScriptFormatter (Formatting)
    """

    def __init__(self, agent, name, method, args, message, loop_data, **kwargs):
        super().__init__(agent, name, method, args, message, loop_data, **kwargs)

    async def execute(self, task: str = "", project_name: str = "", **kwargs):
        """
        Executes a screenwriting task by passing it through a chain of specialized agents.

        Args:
            task (str): The writing task description.
            project_name (str): The name of the project.
        """
        if not task:
            return Response(message="Task description is required.", break_loop=False)

        PrintStyle(font_color="#8E44AD", bold=True).print(f"[{self.agent.agent_name}] Starting production line for project: {project_name}")

        current_input = f"Project: {project_name}\nTask: {task}"
        results = []

        # 1. Structure / Plot Analysis
        # PlotAnalyzer improves or analyzes the structure of the request
        results.append(await self._run_stage(PlotAnalyzer, "Plot Analyzer", "analyze", current_input))
        current_input = results[-1] # Pass output to next stage

        # 2. Creative Ideas
        # CreativeIdeas adds twists or brainstorms based on the analysis
        results.append(await self._run_stage(CreativeIdeas, "Creative Ideas", "brainstorm", current_input))
        current_input = results[-1]

        # 3. Drafting
        # CoWriter drafts the actual content
        results.append(await self._run_stage(CoWriter, "Co-Writer", "draft", current_input))
        current_input = results[-1]

        # 4. Dialogue Evaluation (Optional if not a full script, but we include it in the pipeline)
        # DialogueEvaluator refines the dialogue
        results.append(await self._run_stage(DialogueEvaluator, "Dialogue Evaluator", "evaluate", current_input))
        current_input = results[-1]

        # 5. Formatting
        # ScriptFormatter ensures it is in correct format (HTML/Fountain)
        results.append(await self._run_stage(ScriptFormatter, "Script Formatter", "format", current_input))

        final_output = f"## Production Line Result\n\n{results[-1]}"
        return Response(message=final_output, break_loop=True)

    async def _run_stage(self, AgentClass, stage_name: str, method_name: str, input_text: str) -> str:
        """
        Runs a specific agent stage.
        """
        PrintStyle(font_color="#3498DB").print(f"[{self.agent.agent_name}] Handoff to: {stage_name}")

        # Instantiate the agent
        sub_number = self.agent.number + 1
        sub_agent = AgentClass(sub_number, self.agent.config, self.agent.context)

        # Setup the relationship
        sub_agent.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
        self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub_agent)

        # Ensure the profile is set correctly (folder name matching the agent type usually)
        sub_agent.config.profile = "screenwriting"

        # Call the specific method on the agent
        # We rely on the fact that the agent class has the specific method
        method = getattr(sub_agent, method_name)

        # The methods usually call hist_add_user_message and then monologue
        response = await method(input_text)

        return response
