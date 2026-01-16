from agents import Agent, UserMessage
from python.helpers.tool import Tool, Response
from agents.screenwriting.plot_analyzer import PlotAnalyzer
from agents.screenwriting.creative_ideas import CreativeIdeas
from agents.screenwriting.co_writer import CoWriter
from agents.screenwriting.dialogue_evaluator import DialogueEvaluator
from agents.screenwriting.script_formatter import ScriptFormatter
from agents.screenwriting.world_builder import WorldBuilder
from agents.screenwriting.character_analyzer import CharacterAnalyzer
from agents.screenwriting.pacing_metrics import PacingMetrics
from agents.screenwriting.emotional_tension import EmotionalTension
from agents.screenwriting.marketability import Marketability
from agents.screenwriting.mbti_evaluator import MBTIEvaluator
from agents.screenwriting.scream_analyzer import ScreamAnalyzer
from agents.screenwriting.storyboard_generator import StoryboardGenerator
import json
from python.helpers.print_style import PrintStyle

class ScreenwritingPipeline(Tool):
    """
    Orchestrates a screenwriting pipeline by handing off tasks to specialized agents.
    Each agent handles a specific writing tool process.
    """

    def __init__(self, agent, name, method, args, message, loop_data, **kwargs):
        super().__init__(agent, name, method, args, message, loop_data, **kwargs)

    async def execute(self, task: str = "", project_name: str = "", include_world_building: bool = False, include_character_analysis: bool = False, include_pacing: bool = False, include_tension: bool = False, include_marketability: bool = False, include_mbti: bool = False, include_scream: bool = False, include_storyboard: bool = False, **kwargs):
        """
        Executes a screenwriting task by passing it through a chain of specialized agents.

        Args:
            task (str): The writing task description.
            project_name (str): The name of the project.
            include_world_building (bool): World Building (Lore/Setting).
            include_character_analysis (bool): Character Analysis.
            include_pacing (bool): Pacing Metrics.
            include_tension (bool): Emotional Tension Analysis.
            include_marketability (bool): Marketability Assessment.
            include_mbti (bool): MBTI Evaluation.
            include_scream (bool): Scream Analysis (Horror).
            include_storyboard (bool): Storyboard Generation.
        """
        if not task:
            return Response(message="Task description is required.", break_loop=False)

        PrintStyle(font_color="#8E44AD", bold=True).print(f"[{self.agent.agent_name}] Starting production line for project: {project_name}")

        current_input = f"Project: {project_name}\nTask: {task}"

        # Accumulate results to return a full report if needed
        full_report = []

        # Optional: World Building
        if include_world_building:
             res = await self._run_stage(WorldBuilder, "World Builder", "build", current_input)
             full_report.append(f"## World Building\n{res}")
             current_input += f"\n\nContext from World Builder:\n{res}"

        # Optional: Character Analysis
        if include_character_analysis:
            res = await self._run_stage(CharacterAnalyzer, "Character Analyzer", "analyze", current_input)
            full_report.append(f"## Character Analysis\n{res}")
            current_input += f"\n\nContext from Character Analyzer:\n{res}"

        # 1. Structure / Plot Analysis
        # PlotAnalyzer improves or analyzes the structure of the request
        # The output of PlotAnalyzer is the "Blueprint" for the writing
        plot_analysis = await self._run_stage(PlotAnalyzer, "Plot Analyzer", "analyze", current_input)
        full_report.append(f"## Plot Analysis\n{plot_analysis}")

        # Creative Ideas brainstorming based on plot analysis
        ideas = await self._run_stage(CreativeIdeas, "Creative Ideas", "brainstorm", f"Task: {task}\n\nPlot Analysis:\n{plot_analysis}")
        full_report.append(f"## Creative Ideas\n{ideas}")

        # 2. Drafting
        # CoWriter drafts the actual content based on ideas and plot
        draft_input = f"Task: {task}\n\nPlot Analysis:\n{plot_analysis}\n\nCreative Ideas:\n{ideas}"
        draft = await self._run_stage(CoWriter, "Co-Writer", "draft", draft_input)
        full_report.append(f"## Draft\n{draft}")

        # The Draft is the main artifact we are refining now.
        current_script = draft

        # 3. Optional Analytics (Run on the draft)
        if include_pacing:
            res = await self._run_stage(PacingMetrics, "Pacing Metrics", "analyze", current_script)
            full_report.append(f"## Pacing Metrics\n{res}")

        if include_tension:
            res = await self._run_stage(EmotionalTension, "Emotional Tension", "analyze", current_script)
            full_report.append(f"## Emotional Tension\n{res}")

        if include_scream:
            res = await self._run_stage(ScreamAnalyzer, "Scream Analyzer", "analyze", current_script)
            full_report.append(f"## Scream Analysis\n{res}")

        if include_mbti:
            res = await self._run_stage(MBTIEvaluator, "MBTI Evaluator", "evaluate", current_script)
            full_report.append(f"## MBTI Evaluation\n{res}")

        # 4. Dialogue Evaluation (Refinement)
        # DialogueEvaluator refines the dialogue of the current script
        # We assume DialogueEvaluator returns a critique AND potentially a rewrite if instructed,
        # but to be safe we will pass its output as "Evaluation" and ask Formatter to handle it,
        # OR we treat it as a side-step.
        # If the evaluator returns just critique, we might not want to lose the script.
        # Ideally, CoWriter should have incorporated feedback.
        # Let's assume for this pipeline that DialogueEvaluator provides a "Polished Version" or "Critique".
        # Based on typical agent behavior, it likely returns what was asked.
        # We will append it to the report.
        dialogue_eval = await self._run_stage(DialogueEvaluator, "Dialogue Evaluator", "evaluate", current_script)
        full_report.append(f"## Dialogue Evaluation\n{dialogue_eval}")

        # If the dialogue evaluation contains a rewritten script, we should probably use it.
        # But parsing that is hard. We'll stick to providing the report.

        # 5. Formatting
        # ScriptFormatter ensures it is in correct format (HTML/Fountain)
        formatted_script = await self._run_stage(ScriptFormatter, "Script Formatter", "format", current_script)
        full_report.append(f"## Formatted Script\n{formatted_script}")

        # 6. Post-Script Artifacts
        if include_marketability:
            res = await self._run_stage(Marketability, "Marketability", "assess", formatted_script)
            full_report.append(f"## Marketability Assessment\n{res}")

        if include_storyboard:
            # Storyboard likely needs scene descriptions
            res = await self._run_stage(StoryboardGenerator, "Storyboard Generator", "generate", formatted_script)
            full_report.append(f"## Storyboard\n{res}")

        final_output_str = "\n\n".join(full_report)
        return Response(message=final_output_str, break_loop=True)

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
