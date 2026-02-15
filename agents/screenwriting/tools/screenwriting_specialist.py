from agents import Agent
from python.helpers.tool import Tool, Response
from agents.screenwriting.components.plot_analyzer import PlotAnalyzer
from agents.screenwriting.components.creative_ideas import CreativeIdeas
from agents.screenwriting.components.co_writer import CoWriter
from agents.screenwriting.components.dialogue_evaluator import DialogueEvaluator
from agents.screenwriting.components.script_formatter import ScriptFormatter
from agents.screenwriting.components.character_analyzer import CharacterAnalyzer
from agents.screenwriting.components.pacing_metrics import PacingMetrics
from agents.screenwriting.components.emotional_tension import EmotionalTension
from agents.screenwriting.components.subtext_analyzer import SubtextAnalyzer
from agents.screenwriting.components.marketability import Marketability
from agents.screenwriting.components.mbti_evaluator import MBTIEvaluator
from agents.screenwriting.components.scream_analyzer import ScreamAnalyzer
from agents.screenwriting.components.storyboard_generator import StoryboardGenerator
from agents.screenwriting.components.version_tracker import VersionTracker
from agents.screenwriting.components.world_builder import WorldBuilder
from python.helpers.print_style import PrintStyle


class ScreenwritingSpecialist(Tool):
    """
    Allows direct access to specialized screenwriting agents for specific tasks.
    Available Specialists:
    - PlotAnalyzer: Analyzes plot structure and beats
    - CreativeIdeas: Brainstorms twists and concepts
    - CoWriter: Drafts scenes and chapters
    - DialogueEvaluator: Refines dialogue
    - ScriptFormatter: Formats to Fountain/HTML
    - CharacterAnalyzer: Deep dive into character arcs
    - PacingMetrics: Analyzes story pacing
    - EmotionalTension: Tracks emotional arcs
    - SubtextAnalyzer: Uncovers hidden meanings and motivations
    - Marketability: Assesses commercial potential
    - MBTIEvaluator: Analyzes character personalities
    - WorldBuilder: Develops setting and lore
    - VersionTracker: Keep history of script versions and changes
    """

    def __init__(self, agent, name, method, args,
                 message, loop_data, **kwargs):
        super().__init__(agent, name, method, args, message, loop_data, **kwargs)

    async def execute(self, specialist: str = "", task: str = "", **kwargs):
        """
        Executes a task using a specific specialist agent.

        Args:
            specialist (str): The name of the specialist agent to use.
            task (str): The task for the specialist.
        """
        if not specialist:
            return Response(
                message="Specialist name is required.", break_loop=False)
        if not task:
            return Response(
                message="Task description is required.", break_loop=False)

        specialist_map = {
            "PlotAnalyzer": (PlotAnalyzer, "analyze"),
            "CreativeIdeas": (CreativeIdeas, "brainstorm"),
            "CoWriter": (CoWriter, "draft"),
            "DialogueEvaluator": (DialogueEvaluator, "evaluate"),
            "ScriptFormatter": (ScriptFormatter, "format"),
            "CharacterAnalyzer": (CharacterAnalyzer, "analyze"),
            "PacingMetrics": (PacingMetrics, "analyze"),
            "EmotionalTension": (EmotionalTension, "analyze"),
            "SubtextAnalyzer": (SubtextAnalyzer, "analyze"),
            "Marketability": (Marketability, "assess"),
            "MBTIEvaluator": (MBTIEvaluator, "analyze"),
            "ScreamAnalyzer": (ScreamAnalyzer, "analyze"),
            "StoryboardGenerator": (StoryboardGenerator, "generate"),
            "WorldBuilder": (WorldBuilder, "build"),
            "VersionTracker": (VersionTracker, "record"),
        }

        if specialist not in specialist_map:
            available = ", ".join(specialist_map.keys())
            return Response(
                message=f"Unknown specialist '{specialist}'. Available: {available}", break_loop=False)

        AgentClass, method_name = specialist_map[specialist]

        PrintStyle(font_color="#E67E22", bold=True).print(
            f"[{self.agent.agent_name}] Consulting Specialist: {specialist}")

        # Instantiate the agent
        sub_number = self.agent.number + 1
        sub_agent = AgentClass(
            sub_number,
            self.agent.config,
            self.agent.context)

        # Setup the relationship
        sub_agent.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
        self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub_agent)

        # Ensure the profile is set correctly
        sub_agent.config.profile = "screenwriting"

        # Call the specific method on the agent
        method = getattr(sub_agent, method_name, None)
        if not method:
            return Response(
                message=f"Method '{method_name}' not found on {specialist}.", break_loop=False)

        response = await method(task)

        return Response(
            message=f"## {specialist} Report\n\n{response}", break_loop=True)
