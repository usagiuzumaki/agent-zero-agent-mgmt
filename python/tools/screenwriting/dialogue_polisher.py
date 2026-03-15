from python.helpers.tool import Tool, Response
from agents import Agent, UserMessage

class DialoguePolisher(Tool):
    """
    Refines all dialogue using a subordinate agent.
    """
    def __init__(self, agent: Agent, name="dialogue_polisher", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)

    async def execute(self, **kwargs) -> Response:
        context = self.args.get("context", kwargs.get("context", ""))
        if not context:
            return Response(message="Error: context is required.", break_loop=False)

        if self.agent.get_data(Agent.DATA_NAME_SUBORDINATE) is None:
            sub = Agent(self.agent.number + 1, self.agent.config, self.agent.context)
            sub.set_data(Agent.DATA_NAME_SUPERIOR, self.agent)
            self.agent.set_data(Agent.DATA_NAME_SUBORDINATE, sub)

        subordinate: Agent = self.agent.get_data(Agent.DATA_NAME_SUBORDINATE)
        instruction = f"You are a Screenwriting Specialist: Dialogue Polisher. Polish the dialogue in this context to ensure strong subtext and character voice.\nContext:\n{context}"
        subordinate.hist_add_user_message(UserMessage(message=instruction, attachments=[]))

        result = await subordinate.monologue()
        return Response(message=result, break_loop=False)
