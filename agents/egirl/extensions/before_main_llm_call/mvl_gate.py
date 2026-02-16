import asyncio
from python.helpers.extension import Extension
from python.helpers.mvl_manager import MVLManager
from python.helpers.print_style import PrintStyle
from python.helpers.errors import SilentResponseException
from python.helpers import history

class MVLGate(Extension):

    async def execute(self, loop_data, **kwargs):
        # We only want to run this for the main agent, and only if it's processing a user message.
        if not loop_data.user_message:
            return

        # Only check gate on the first iteration of the message loop
        if loop_data.iteration > 0:
            return

        user_id = self.agent.context.id

        # Extract text from message content
        content = loop_data.user_message.content
        if isinstance(content, str):
            text = content
        elif isinstance(content, list):
            # Extract text parts
            text = " ".join([c.get("text", "") for c in content if isinstance(c, dict) and "text" in c])
        elif isinstance(content, dict):
            text = content.get("text", str(content))
        else:
            text = str(content)

        if not text.strip():
            return # Skip empty messages

        # Initialize manager
        manager = MVLManager(agent=self.agent)

        # Process message
        PrintStyle(font_color="#b3ffd9", padding=False).print("MVL: Analyzing...")

        # We need to await process_message
        gate = await manager.process_message(user_id, text)

        PrintStyle(font_color="#b3ffd9", padding=False).print(f"MVL: Gate decision = {gate}")

        if gate == "silence":
            raise SilentResponseException("MVL Gate: silence")

        if gate == "delay":
            PrintStyle(font_color="#b3ffd9", padding=False).print("MVL: Delaying response...")
            await asyncio.sleep(3) # Short delay for effect

        if gate == "confront":
            # Inject system prompt
            confrontation_prompt = "Your narrative analysis suggests a confrontation is needed. Be direct and challenge the user's assumptions."
            loop_data.system.append(confrontation_prompt)
            PrintStyle(font_color="#b3ffd9", padding=False).print("MVL: Confrontation mode active.")
