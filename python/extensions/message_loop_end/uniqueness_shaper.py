from python.helpers.extension import Extension
from python.uniqueness.engine import AriaUniquenessEngine

class UniquenessShaper(Extension):
    async def execute(self, loop_data, **kwargs):
        enabled = self.agent.config.additional.get("UNIQUENESS_ENGINE", False) or getattr(self.agent.config, 'uniqueness_engine', False)

        if not enabled:
            return

        engine = self.agent.get_data("uniqueness_engine")
        if not engine:
            return

        # Shaping the last response
        if loop_data.last_response:
            user_input = ""
            if loop_data.user_message:
                try:
                    user_input = str(loop_data.user_message.content)
                except:
                    user_input = ""

            shaped_response = await engine.process_response(
                self.agent,
                user_input,
                loop_data.last_response
            )
            loop_data.last_response = shaped_response
