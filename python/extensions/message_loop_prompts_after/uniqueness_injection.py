from python.helpers.extension import Extension
from python.uniqueness.engine import AriaUniquenessEngine

class UniquenessInjection(Extension):
    async def execute(self, loop_data, **kwargs):
        # Use UNIQUENESS_ENGINE from additional config or the dedicated field
        enabled = self.agent.config.additional.get("UNIQUENESS_ENGINE", False) or getattr(self.agent.config, 'uniqueness_engine', False)

        if not enabled:
            return

        # Initialize engine if not already in agent data
        engine = self.agent.get_data("uniqueness_engine")
        if not engine:
            engine = AriaUniquenessEngine()
            self.agent.set_data("uniqueness_engine", engine)

        # Get snippet and inject into system prompt
        snippet = await engine.get_system_prompt_snippet()
        if snippet:
            loop_data.system.append(snippet)
