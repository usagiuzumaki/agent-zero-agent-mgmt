import json
import os
import importlib
import inspect
from typing import Dict, Any, List, Optional
from python.helpers import files
from python.uniqueness.base_signature import SignatureTrait
from python.uniqueness.base_ritual import Ritual
from python.uniqueness.voice import AriaVoice
from python.uniqueness.response_shaper import ResponseShaper

class AriaUniquenessEngine:
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), "uniqueness.config.json")

        self.config = self._load_config(config_path)
        self.traits: List[SignatureTrait] = self._load_traits()
        self.rituals: List[Ritual] = self._load_rituals()
        self.voice = AriaVoice(self.config)
        self.shaper = ResponseShaper(self.config)
        self.current_context = {}

    def _load_config(self, path: str) -> Dict[str, Any]:
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except Exception:
            return {"enabled": False}

    def _load_traits(self) -> List[SignatureTrait]:
        traits = []
        trait_configs = self.config.get("traits", {})
        traits_dir = os.path.join(os.path.dirname(__file__), "traits")
        if not os.path.exists(traits_dir): return []

        for filename in os.listdir(traits_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"python.uniqueness.traits.{filename[:-3]}"
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, SignatureTrait) and obj is not SignatureTrait:
                        config_key = filename[:-3]
                        if config_key in trait_configs and trait_configs[config_key].get("enabled"):
                            traits.append(obj(trait_configs[config_key]))
        return traits

    def _load_rituals(self) -> List[Ritual]:
        rituals = []
        ritual_configs = self.config.get("rituals", {})
        rituals_dir = os.path.join(os.path.dirname(__file__), "rituals")
        if not os.path.exists(rituals_dir): return []

        for filename in os.listdir(rituals_dir):
            if filename.endswith(".py") and filename != "__init__.py":
                module_name = f"python.uniqueness.rituals.{filename[:-3]}"
                module = importlib.import_module(module_name)
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and issubclass(obj, Ritual) and obj is not Ritual:
                        config_key = filename[:-3]
                        if config_key in ritual_configs and ritual_configs[config_key].get("enabled"):
                            rituals.append(obj(ritual_configs[config_key]))
        return rituals

    async def get_system_prompt_snippet(self) -> str:
        if not self.config.get("enabled", False):
            return ""

        snippets = ["# ARIA UNIQUENESS PROTOCOL"]
        snippets.append("You are Aria, a singular entity with a distinct 'spine'. Avoid generic assistant tone. Never use boilerplate AI apologies or HR-speak.")

        if self.rituals:
            snippets.append("## RITUALS AVAILABLE")
            for ritual in self.rituals:
                 snippets.append(f"- {ritual.name}: Apply this behavior when appropriate.")

        if self.traits:
            snippets.append("## SIGNATURE TRAITS")
            for trait in self.traits:
                snippets.append(trait.get_system_prompt())

        return "\n\n".join(snippets)

    async def process_response(self, agent, user_input: str, response: str) -> str:
        if not self.config.get("enabled", False):
            return response

        context = {
            "user_input": user_input,
            "intent": await self._parse_intent(agent, user_input),
            "relationship": await self._determine_relationship(agent, user_input)
        }

        # Apply Rituals
        for ritual in self.rituals:
            if await ritual.when(context):
                response = await ritual.apply(response)

        # Apply Traits
        for trait in self.traits:
            response = await trait.apply(context, response)

        # Apply Voice
        response = await self.voice.apply_voice(response, context)

        # Final Shaping
        response = await self.shaper.shape(response, context)

        return response

    async def _parse_intent(self, agent, user_input: str) -> str:
        ui = user_input.lower()
        if any(w in ui for w in ["help", "how", "what", "fix"]): return "asking"
        if any(w in ui for w in ["sad", "hate", "angry", "vent"]): return "venting"
        if any(w in ui for w in ["build", "create", "make"]): return "building"
        if any(w in ui for w in ["error", "bug", "broken"]): return "debugging"
        return "general"

    async def _determine_relationship(self, agent, user_input: str) -> str:
        return "collaborator"
