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
from agents.screenwriting.mbti_evaluator import MBTIEvaluator
from agents.screenwriting.scream_analyzer import ScreamAnalyzer
from agents.screenwriting.storyboard_generator import StoryboardGenerator
from agents.screenwriting.marketability import Marketability
from python.helpers.print_style import PrintStyle


class ScreenwritingPipeline(Tool):
    """
    Orchestrates a screenwriting pipeline by handing off tasks to specialized agents.
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
    7. PacingMetrics (Analysis) - Optional
    8. EmotionalTension (Analysis) - Optional
    9. MBTIEvaluator (Analysis) - Optional
    10. ScreamAnalyzer (Analysis) - Optional
    11. ScriptFormatter (Formatting)
    12. Marketability (Analysis) - Optional
    13. StoryboardGenerator (Analysis) - Optional
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
                      include_emotional_tension: bool = False,
                      include_mbti_evaluator: bool = False,
                      include_scream_analysis: bool = False,
                      include_marketability: bool = False,
                      include_storyboard_generator: bool = False,
                      **kwargs):
        """
        Executes a screenwriting task by passing it through a chain of specialized agents.

        Args:
            task (str): The writing task description.
            project_name (str): The name of the project.
            include_world_building (bool): Whether to include a world building step.
            include_character_analysis (bool): Whether to include a character analysis step.
            include_pacing (bool): Include pacing metrics analysis.
            include_emotional_tension (bool): Include emotional tension analysis.
            include_mbti_evaluator (bool): Include MBTI personality evaluation.
            include_scream_analysis (bool): Include scream/intensity analysis.
            include_marketability (bool): Include marketability assessment.
            include_storyboard_generator (bool): Include storyboard generation.
        """
        if not task:
            return Response(
                message="Task description is required.",
                break_loop=False)

        PrintStyle(font_color="#8E44AD", bold=True).print(
            f"[{self.agent.agent_name}] Starting production line for project: {project_name}")

        current_input = f"Project: {project_name}\nTask: {task}"
        results = []
        analysis_outputs = []

        # Optional: World Building
        if include_world_building:
            results.append(await self._run_stage(WorldBuilder, "World Builder", "build", current_input))
            current_input = results[-1]

        # Optional: Character Analysis
        if include_character_analysis:
            results.append(await self._run_stage(CharacterAnalyzer, "Character Analyzer", "analyze", current_input))
            current_input = results[-1]

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
        current_script = current_input

        # Optional Analysis Phase (Non-Transformative)
        if include_pacing:
             analysis_outputs.append(await self._run_stage(PacingMetrics, "Pacing Metrics", "analyze", current_script))

        if include_tension:
             analysis_outputs.append(await self._run_stage(EmotionalTension, "Emotional Tension", "analyze", current_script))

        if include_scream:
             analysis_outputs.append(await self._run_stage(ScreamAnalyzer, "Scream Analyzer", "analyze", current_script))

        if include_mbti:
             analysis_outputs.append(await self._run_stage(MBTIEvaluator, "MBTI Evaluator", "analyze", current_script))

        if include_marketability:
             analysis_outputs.append(await self._run_stage(Marketability, "Marketability", "analyze", current_script))

        if include_storyboard:
             analysis_outputs.append(await self._run_stage(StoryboardGenerator, "Storyboard Generator", "analyze", current_script))

        # 4. Dialogue Evaluation (Transformative)
        # DialogueEvaluator refines the dialogue
        results.append(await self._run_stage(DialogueEvaluator, "Dialogue Evaluator", "evaluate", current_input))
        current_input = results[-1]

        # Analysis stages (Do not update current_input)
        if include_pacing:
            results.append(await self._run_stage(PacingMetrics, "Pacing Metrics", "analyze", current_input))

        if include_emotional_tension:
            results.append(await self._run_stage(EmotionalTension, "Emotional Tension", "analyze", current_input))

        if include_mbti:
            results.append(await self._run_stage(MBTIEvaluator, "MBTI Evaluator", "analyze", current_input))

        if include_scream_analysis:
            results.append(await self._run_stage(ScreamAnalyzer, "Scream Analyzer", "analyze", current_input))

        # 5. Formatting
        results.append(await self._run_stage(ScriptFormatter, "Script Formatter", "format", current_input))
        # Note: We update current_input here, though formatting might be the
        # final text form we want for marketability too.
        current_input = results[-1]

        # --- Optional Post-Production Analysis ---

        if include_marketability:
            results.append(await self._run_stage(Marketability, "Marketability", "analyze", current_input))

        if include_storyboard:
            results.append(await self._run_stage(StoryboardGenerator, "Storyboard Generator", "analyze", current_input))

        # Return full report containing all steps
        full_report = "\n\n---\n\n".join(results)
        return Response(
            message=f"## Production Line Complete\n\n{full_report}",
            break_loop=True)

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
