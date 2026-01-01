from agents import Agent, UserMessage
from python.helpers.tool import Tool, Response
from python.helpers import extract_tools, files
import json

class ScreenwritingProduction(Tool):
    """
    Orchestrates a screenwriting production line by handing off tasks to specialized agents.
    """

    async def execute(self, task: str = "", project_name: str = "", **kwargs):
        """
        Executes a screenwriting task by passing it through a chain of specialized agents.

        Args:
            task (str): The writing task description.
            project_name (str): The name of the project.
        """
        if not task:
            return Response(message="Task description is required.", break_loop=False)

        # Define the production line stages
        # We will use the Agent class with specific profiles from agents/screenwriting/
        # The profiles are directories like agents/screenwriting/prompts/ (if structured that way)
        # OR we use the specialized classes if we can instantiate them.

        # Checking how specialized agents are loaded.
        # agents/screenwriting/base.py defines ScreenwritingAgent.
        # agents/screenwriting/plot_analyzer.py defines PlotAnalyzer.

        # Since the Agent system seems to be designed around profiles loading prompts,
        # but here we have specific python classes.
        # The 'Delegation' tool (call_subordinate) instantiates 'Agent'.

        # We will manually instantiate the sequence of agents.
        # For this prototype, we will implement a simple flow:
        # 1. Structure Analysis (PlotAnalyzer)
        # 2. Drafting (CoWriter - assuming it exists or using base)
        # 3. Review (DialogueEvaluator)

        results = []
        current_input = f"Project: {project_name}\nTask: {task}"

        # 1. Structure / Plot Analysis
        results.append(await self._run_stage("Plot Analyzer", "screenwriting", "plot_analyzer", current_input))
        current_input = results[-1]

        # 2. Drafting / Creative Ideas (using CreativeIdeas as an example of next step)
        results.append(await self._run_stage("Creative Ideas", "screenwriting", "creative_ideas", current_input))
        current_input = results[-1]

        # 3. Formatting (ScriptFormatter)
        results.append(await self._run_stage("Script Formatter", "screenwriting", "script_formatter", current_input))

        final_output = f"## Production Line Result\n\n{results[-1]}"
        return Response(message=final_output, break_loop=True)

    async def _run_stage(self, stage_name: str, profile_group: str, agent_file_name: str, input_text: str) -> str:
        """
        Runs a specific agent stage.
        """
        print(f"[{self.agent.agent_name}] Starting stage: {stage_name}")

        # Create a subordinate agent
        # We want to use the specialized class if possible, but 'Agent' constructor is standard.
        # If we want to use PlotAnalyzer class, we need to import it.

        # Dynamic import of the agent class
        try:
            # e.g. agents/screenwriting/plot_analyzer.py
            module_path = f"agents/{profile_group}/{agent_file_name}.py"
            # We need to find the class name. Usually PascalCase of snake_case file.
            class_name = "".join(x.title() for x in agent_file_name.split("_"))

            classes = extract_tools.load_classes_from_file(module_path, Agent)
            if not classes:
                # Fallback to standard Agent if specialized class not found
                AgentClass = Agent
            else:
                AgentClass = classes[0]

        except Exception as e:
            print(f"Error loading agent class for {agent_file_name}: {e}. Using standard Agent.")
            AgentClass = Agent

        # Instantiate the agent
        # Subordinate agents are usually numbered relative to parent
        sub_number = self.agent.number + 1
        sub_agent = AgentClass(sub_number, self.agent.config, self.agent.context)

        # Setup the relationship
        sub_agent.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
        self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub_agent)

        # Set the profile if using standard Agent, or if the specialized agent relies on it
        # The 'screenwriting' profile folder exists (agents/screenwriting)
        sub_agent.config.profile = profile_group

        # Add the message
        prompt = f"You are acting as the {stage_name}. Please process the following input:\n\n{input_text}"
        sub_agent.hist_add_user_message(UserMessage(message=prompt))

        # Run monologue
        response = await sub_agent.monologue()
        return response
