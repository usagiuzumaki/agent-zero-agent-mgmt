import json
from agents import LoopData
from python.helpers.extension import Extension
from python.helpers.aria_welcome import get_initial_message_json


class InitialMessage(Extension):

    async def execute(self, **kwargs):
        """
        Add an initial greeting message when first user message is processed.
        Called only once per session via _process_chain method.
        """

        # Only add initial message for main agent (A0), not subordinate agents
        if self.agent.number != 0:
            return

        # If the context already contains log messages, do not add another initial message
        if self.agent.context.log.logs:
            return

        # Generate personalized welcome message using Aria's welcome system
        initial_message_json = get_initial_message_json()
        initial_message = json.dumps(initial_message_json)
        initial_message_text = initial_message_json.get("tool_args", {}).get("text", "Hello! 💕 I'm Aria, your AI companion!")

        # add initial loop data to agent (for hist_add_ai_response)
        self.agent.loop_data = LoopData(user_message=None)

        # Add the message to history as an AI response
        self.agent.hist_add_ai_response(initial_message)

        # Add to log (green bubble) for immediate UI display
        self.agent.context.log.log(
            type="response",
            heading="Aria: Welcome",  # Always use "Aria" branding
            content=initial_message_text,
            finished=True,
            update_progress="none",
        )
