from typing import Dict, Any

class ResponseShaper:
    def __init__(self, engine_config: Dict[str, Any]):
        self.config = engine_config

    async def shape(self, response: str, context: Dict[str, Any]) -> str:
        # Ensure output remains useful, structured, and not overwritten by style.
        # v1: Basic cleanup
        response = response.strip()

        # Ensure it doesn't end abruptly if rituals added content
        if not response.endswith(('.', '!', '?', ')')):
            # potentially fix if it looks like a truncated sentence
            pass

        return response
