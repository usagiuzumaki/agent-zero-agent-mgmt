from python.helpers.extension import Extension
from python.helpers.errors import SilentResponseException
from python.helpers.print_style import PrintStyle

class MVLProcessor(Extension):
    async def execute(self, loop_data, **kwargs):
        if not hasattr(self.agent, "mvl"):
            return

        user_id = getattr(self.agent.context, "user_id", "default_user")
        text = ""
        if loop_data.user_message:
            # history.Message content can be str or dict
            content = loop_data.user_message.content
            if isinstance(content, dict):
                text = content.get("message", "")
            else:
                text = str(content)

        if not text:
            return

        gate = await self.agent.mvl.process_message(user_id, text)

        if gate == "silence":
            raise SilentResponseException("MVL Decision: Silence")
        elif gate == "refuse":
            loop_data.params_temporary["mvl_instruction"] = "REFUSE: Be polite but distant. Do not engage deeply with the user's emotional or complex requests at this time."
        elif gate == "confront":
            loop_data.params_temporary["mvl_instruction"] = "CONFRONT: Address the user's recurring patterns, contradictions, or behaviors directly. Be firm and analytical."
