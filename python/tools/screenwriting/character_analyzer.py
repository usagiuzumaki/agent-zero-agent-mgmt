from python.helpers.tool import Tool, Response
from agents import Agent, UserMessage

class CharacterAnalyzer(Tool):
    """
    Analyzes or generates characters for scenes using a subordinate agent.
    """
    def __init__(self, agent: Agent, name="character_analyzer", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        context = self.args.get("context", kwargs.get("context", ""))
        if not context:
            return Response(message="Error: context is required.", break_loop=False)

        # Delegate to a subordinate Agent Zero process
        if self.agent.get_data(Agent.DATA_NAME_SUBORDINATE) is None:
            sub = Agent(self.agent.number + 1, self.agent.config, self.agent.context)
            sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
            self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub)

        subordinate: Agent = self.agent.get_data(Agent.DATA_NAME_SUBORDINATE)

        # In this task we should map writers_room logic into these real prompts but doing it via actual agent invocation.
        instruction = f"You are a Screenwriting Specialist: Character Analyzer. Analyze the characters in this context. Output a character map and their motivations.\nContext:\n{context}"
        subordinate.hist_add_user_message(UserMessage(message=instruction, attachments=[]))

        # run subordinate monologue
        result = await subordinate.monologue()

        return Response(message=result, break_loop=False)
