from abc import ABC, abstractmethod
from typing import Any, Dict

class Ritual(ABC):
    def __init__(self, config: Dict[str, Any]):
        self.config = config

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    async def when(self, context: Dict[str, Any]) -> bool:
        pass

    @abstractmethod
    async def apply(self, response: str) -> str:
        pass
