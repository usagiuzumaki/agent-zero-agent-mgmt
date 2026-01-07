from agents import Agent
from python.helpers.tool import Tool, Response
from python.helpers.print_style import PrintStyle
import json
import inspect

# Import all screenwriting agents
from agents.screenwriting.plot_analyzer import PlotAnalyzer
from agents.screenwriting.creative_ideas import CreativeIdeas
from agents.screenwriting.co_writer import CoWriter
from agents.screenwriting.dialogue_evaluator import DialogueEvaluator
from agents.screenwriting.script_formatter import ScriptFormatter
from agents.screenwriting.character_analyzer import CharacterAnalyzer
from agents.screenwriting.emotional_tension import EmotionalTension
from agents.screenwriting.marketability import Marketability
from agents.screenwriting.mbti_evaluator import MBTIEvaluator
from agents.screenwriting.pacing_metrics import PacingMetrics
from agents.screenwriting.scream_analyzer import ScreamAnalyzer
from agents.screenwriting.storyboard_generator import StoryboardGenerator
from agents.screenwriting.version_tracker import VersionTracker
from agents.screenwriting.world_builder import WorldBuilder


class ScreenwritingSpecialist(Tool):
    """
    Directly invokes a specialized screenwriting agent for a specific task.
    This allows utilizing specific tools like Character Analyzer, World Builder, etc., individually.
    """

    # Map of agent names to (Class, method_name, is_async_monologue)
    # is_async_monologue: True if it calls self.monologue() (returns str via LLM)
    #                     False if it just returns a result directly (like PacingMetrics)
    AGENTS_MAP = {
        "plot_analyzer": (PlotAnalyzer, "analyze", True),
        "creative_ideas": (CreativeIdeas, "brainstorm", True),
        "co_writer": (CoWriter, "draft", True),
        "dialogue_evaluator": (DialogueEvaluator, "evaluate", True),
        "script_formatter": (ScriptFormatter, "format", True),
        "character_analyzer": (CharacterAnalyzer, "analyze", True),
        "emotional_tension": (EmotionalTension, "gauge", True),
        "marketability": (Marketability, "assess", True),
        "mbti_evaluator": (MBTIEvaluator, "evaluate", False),
        "pacing_metrics": (PacingMetrics, "compute", False),
        "scream_analyzer": (ScreamAnalyzer, "analyze", True),
        "storyboard_generator": (StoryboardGenerator, "generate", True),
        "version_tracker": (VersionTracker, "record", True),
        "world_builder": (WorldBuilder, "check", True),
    }

    async def execute(self, agent_name: str, instruction: str, **kwargs):
        """
        Executes a task using a specific screenwriting specialist agent.

        Args:
            agent_name (str): The name of the agent to use (e.g., 'character_analyzer', 'world_builder').
            instruction (str): The input text or instruction for the agent.
        """
        agent_name = agent_name.lower().replace(" ", "_")

        if agent_name not in self.AGENTS_MAP:
            valid_agents = ", ".join(self.AGENTS_MAP.keys())
            return Response(message=f"Unknown agent '{agent_name}'. Valid agents are: {valid_agents}", break_loop=False)

        AgentClass, method_name, is_async_monologue = self.AGENTS_MAP[agent_name]

        PrintStyle(font_color="#3498DB").print(f"[{self.agent.agent_name}] Calling Specialist: {AgentClass.__name__}")

        # Instantiate the agent
        sub_number = self.agent.number + 1
        sub_agent = AgentClass(sub_number, self.agent.config, self.agent.context)

        # Setup relationship
        sub_agent.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
        self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub_agent)
        sub_agent.config.profile = "screenwriting"

        # Get the method
        method = getattr(sub_agent, method_name)

        try:
            if is_async_monologue:
                # Async method that likely uses LLM monologue
                response = await method(instruction)
            else:
                # Synchronous method or direct return (like PacingMetrics)
                if inspect.iscoroutinefunction(method):
                     response = await method(instruction)
                else:
                     response = method(instruction)

                # Format dict response if needed
                if isinstance(response, dict):
                    response = json.dumps(response, indent=2)

            return Response(message=str(response), break_loop=True)

        except Exception as e:
            return Response(message=f"Error executing {agent_name}: {str(e)}", break_loop=False)
