from agents import Agent
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
from python.helpers.print_style import PrintStyle


class ScreenwritingPipeline(Tool):
    """
    Orchestrates a screenwriting pipeline by handing off tasks to specialized agents.
    This serves as the subordinate agent process that hands the writing down from one agent
    to the next in charge of each writing tool process.

    Each agent handles a specific writing tool process:
    1. WorldBuilder (Setting/Lore) - Optional
    2. CharacterAnalyzer (Characters) - Optional
    3. PlotAnalyzer (Structure)
    4. CreativeIdeas (Brainstorming)
    5. CoWriter (Drafting)
    6. DialogueEvaluator (Refinement)
    7. Analysis Agents (Pacing, Tension, MBTI, Scream) - Optional
    8. ScriptFormatter (Formatting)
    9. Post-Production Agents (Marketability, Storyboard) - Optional
    """

    def __init__(
            self,
            agent,
            name,
            method,
            args,
            message,
            loop_data,
            **kwargs):
        super().__init__(agent, name, method, args, message, loop_data, **kwargs)

    async def execute(self, task: str = "", project_name: str = "",
                      include_world_building: bool = False,
                      include_character_analysis: bool = False,
                      include_pacing: bool = False,
                      include_tension: bool = False,
                      include_marketability: bool = False,
                      include_mbti: bool = False,
                      include_scream: bool = False,
                      include_storyboard: bool = False,
                      **kwargs):
        """
        Executes a screenwriting task by passing it through a chain of specialized agents.

        Args:
            task (str): The writing task description.
            project_name (str): The name of the project.
            include_world_building (bool): Whether to include a world building step.
            include_character_analysis (bool): Whether to include a character analysis step.
            include_pacing (bool): Whether to include pacing metrics.
            include_tension (bool): Whether to include emotional tension analysis.
            include_marketability (bool): Whether to include marketability assessment.
            include_mbti (bool): Whether to include MBTI evaluation.
            include_scream (bool): Whether to include scream/intensity analysis.
            include_storyboard (bool): Whether to include storyboard generation.
        """
        if not task:
            return Response(
                message="Task description is required.",
                break_loop=False)

        PrintStyle(font_color="#8E44AD", bold=True).print(
            f"[{self.agent.agent_name}] Starting production line for project: {project_name}")

        current_input = f"Project: {project_name}\nTask: {task}"
        results = []
        analysis_reports = []

        # Optional: World Building
        if include_world_building:
            results.append(await self._run_stage(WorldBuilder, "World Builder", "build", current_input))
            current_input = results[-1]

        # Optional: Character Analysis
        if include_character_analysis:
            results.append(await self._run_stage(CharacterAnalyzer, "Character Analyzer", "analyze", current_input))
            current_input = results[-1]

            # MBTI is best run on character analysis output or raw description if available here
            if include_mbti:
                report = await self._run_stage(MBTIEvaluator, "MBTI Evaluator", "analyze", current_input)
                analysis_reports.append(report)

        # 1. Structure / Plot Analysis
        results.append(await self._run_stage(PlotAnalyzer, "Plot Analyzer", "analyze", current_input))
        current_input = results[-1]  # Pass output to next stage

        # 2. Creative Ideas
        results.append(await self._run_stage(CreativeIdeas, "Creative Ideas", "brainstorm", current_input))
        current_input = results[-1]

        # 3. Drafting
        # CoWriter drafts the actual content
        draft_result = await self._run_stage(CoWriter, "Co-Writer", "draft", current_input)
        results.append(draft_result)
        current_input = draft_result

        # 4. Dialogue Evaluation
        # DialogueEvaluator refines the dialogue
        results.append(await self._run_stage(DialogueEvaluator, "Dialogue Evaluator", "evaluate", current_input))
        current_input = results[-1]
        draft_text = current_input

        # Intermediate Analysis (on the refined draft)
        if include_pacing:
            report = await self._run_stage(PacingMetrics, "Pacing Metrics", "analyze", draft_text)
            analysis_reports.append(report)

        if include_tension:
            report = await self._run_stage(EmotionalTension, "Emotional Tension", "analyze", draft_text)
            analysis_reports.append(report)

        if include_scream:
            report = await self._run_stage(ScreamAnalyzer, "Scream Analyzer", "analyze", draft_text)
            analysis_reports.append(report)

        # Optional MBTI on script if not run on characters (or run again on script)
        if include_mbti and not include_character_analysis:
             report = await self._run_stage(MBTIEvaluator, "MBTI Evaluator", "analyze", draft_text)
             analysis_reports.append(report)

        # 5. Formatting
        results.append(await self._run_stage(ScriptFormatter, "Script Formatter", "format", current_input))
        formatted_script = results[-1]

        # Final Analysis/Generation (on the formatted script or draft)
        if include_marketability:
            report = await self._run_stage(Marketability, "Marketability", "assess", draft_text)
            analysis_reports.append(report)

        if include_storyboard:
            report = await self._run_stage(StoryboardGenerator, "Storyboard Generator", "generate", draft_text)
            analysis_reports.append(report)

        final_output = f"## Production Line Result\n\n{formatted_script}"

        if analysis_reports:
            final_output += "\n\n---\n\n## Analysis & Extras\n\n" + "\n\n".join(analysis_reports)

        return Response(message=final_output, break_loop=True)

    async def _run_stage(
            self,
            AgentClass,
            stage_name: str,
            method_name: str,
            input_text: str) -> str:
        """
        Runs a specific agent stage.
        """
        PrintStyle(font_color="#3498DB").print(
            f"[{self.agent.agent_name}] Handoff to: {stage_name}")

        # Instantiate the agent
        sub_number = self.agent.number + 1
        sub_agent = AgentClass(
            sub_number,
            self.agent.config,
            self.agent.context)

        # Setup the relationship
        sub_agent.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
        self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub_agent)

        # Ensure the profile is set correctly (folder name matching the agent
        # type usually)
        sub_agent.config.profile = "screenwriting"

        # Call the specific method on the agent
        method = getattr(sub_agent, method_name)

        # The methods usually call hist_add_user_message and then monologue
        response = await method(input_text)

        return response
