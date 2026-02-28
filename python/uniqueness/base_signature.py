from abc import ABC, abstractmethod
from typing import Any, Dict

class SignatureTrait(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.strength = config.get("strength", 0.5)

    @abstractmethod
    async def apply(self, context: Dict[str, Any], draft_response: str) -> str:
        pass

    @abstractmethod
    def get_system_prompt(self) -> str:
        pass
