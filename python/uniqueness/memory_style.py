from typing import Dict, Any, List, Optional
import json

class AriaMemoryStyle:
    def __init__(self, engine_config: Dict[str, Any]):
        self.config = engine_config

    async def should_store_memory(self, message: str, context: Dict[str, Any]) -> bool:
        # v1: Logic to decide if something is worth remembering
        important_keywords = ["prefer", "love", "hate", "always", "never", "project", "work on"]
        msg_lower = message.lower()
        return any(kw in msg_lower for kw in important_keywords)

    async def summarize_memory(self, message: str, context: Dict[str, Any]) -> str:
        # Returns structured JSON in Aria's voice
        # In a real implementation, this might call a utility model
        summary_data = {
            "type": "preference",
            "summary": "User expressed a specific preference/detail.",
            "why_useful": "To maintain continuity and personal resonance.",
            "tags": ["aria-uniqueness", "v1"]
        }
        return json.dumps(summary_data)

    def get_test_set(self) -> List[Dict[str, Any]]:
        return [
            {"message": "I love working on Python projects at night.", "expected_store": True},
            {"message": "What time is it?", "expected_store": False},
            {"message": "I hate being called 'assistant'.", "expected_store": True},
            {"message": "My new project is called Operation Labyrinth.", "expected_store": True},
            {"message": "I'm just venting, I feel stuck.", "expected_store": False},
            {"message": "Always use 2 spaces for indentation.", "expected_store": True},
            {"message": "Never mention the war.", "expected_store": True},
            {"message": "Let's build a new engine.", "expected_store": True},
            {"message": "I'm going for a walk.", "expected_store": False},
            {"message": "I prefer dark mode.", "expected_store": True}
        ]
