import json
import os
from typing import Optional, Dict, Any

from python.helpers.tool import Tool, Response
from agents import Agent

# Tool schemas

inject_fourth_wall_break_schema = {
    "name": "inject_fourth_wall_break",
    "description": "Inject a meta-humorous fourth wall break into the scene.",
    "parameters": {
        "type": "object",
        "properties": {
            "character": {"type": "string", "description": "The character breaking the fourth wall"},
            "target_line": {"type": "string", "description": "The line or beat to interject on"},
            "meta_commentary": {"type": "string", "description": "The meta-humor commentary to insert"}
        },
        "required": ["character", "meta_commentary"]
    }
}

format_action_sequence_schema = {
    "name": "format_action_sequence",
    "description": "Format a high-octane action sequence to improve pacing.",
    "parameters": {
        "type": "object",
        "properties": {
            "characters_involved": {"type": "array", "items": {"type": "string"}},
            "action_beats": {"type": "array", "items": {"type": "string"}, "description": "The rapid-fire action beats"},
            "pacing_notes": {"type": "string"}
        },
        "required": ["characters_involved", "action_beats"]
    }
}

generate_character_motivation_schema = {
    "name": "generate_character_motivation",
    "description": "Generate deep psychological and mystical motivation for a character's actions.",
    "parameters": {
        "type": "object",
        "properties": {
            "character": {"type": "string"},
            "action": {"type": "string", "description": "The action to motivate"},
            "tarot_archetype": {"type": "string", "description": "The archetype driving them"},
            "hidden_motivation": {"type": "string"}
        },
        "required": ["character", "action", "hidden_motivation"]
    }
}

escalate_tension_schema = {
    "name": "escalate_tension",
    "description": "Escalate the dramatic tension in preparation for the climax.",
    "parameters": {
        "type": "object",
        "properties": {
            "current_stakes": {"type": "string"},
            "new_stakes": {"type": "string", "description": "The escalated stakes"},
            "turning_point": {"type": "string", "description": "The precise beat where the chips are pushed in"}
        },
        "required": ["new_stakes", "turning_point"]
    }
}

write_dialogue_schema = {
    "name": "write_dialogue",
    "description": "Write a snippet of dialogue between characters.",
    "parameters": {
        "type": "object",
        "properties": {
            "character1": {"type": "string"},
            "character2": {"type": "string"},
            "dialogue_snippet": {"type": "string"}
        },
        "required": ["character1", "dialogue_snippet"]
    }
}

optimize_pacing_schema = {
    "name": "optimize_pacing",
    "description": "Optimize the pacing of a scene.",
    "parameters": {
        "type": "object",
        "properties": {
            "scene_text": {"type": "string"},
            "optimizations": {"type": "string"}
        },
        "required": ["scene_text", "optimizations"]
    }
}

weave_backstory_schema = {
    "name": "weave_backstory",
    "description": "Weave a character's backstory into the current scene.",
    "parameters": {
        "type": "object",
        "properties": {
            "character": {"type": "string"},
            "backstory_element": {"type": "string"}
        },
        "required": ["character", "backstory_element"]
    }
}

write_climax_schema = {
    "name": "write_climax",
    "description": "Write the climax of a scene or act.",
    "parameters": {
        "type": "object",
        "properties": {
            "build_up": {"type": "string"},
            "climax_event": {"type": "string"}
        },
        "required": ["climax_event"]
    }
}


generate_plot_twist_schema = {
    "name": "generate_plot_twist",
    "description": "Generate an unpredictable plot twist.",
    "parameters": {
        "type": "object",
        "properties": {
            "current_scenario": {"type": "string"},
            "twist_type": {"type": "string", "description": "Type of twist (e.g., betrayal, revelation, shifting reality)"},
            "twist_description": {"type": "string"}
        },
        "required": ["current_scenario", "twist_description"]
    }
}

rewrite_from_perspective_schema = {
    "name": "rewrite_from_perspective",
    "description": "Rewrite a scene from an entirely different, unexpected character's point of view.",
    "parameters": {
        "type": "object",
        "properties": {
            "scene_text": {"type": "string"},
            "new_perspective_character": {"type": "string", "description": "The unexpected character or object"},
            "rewritten_scene": {"type": "string"}
        },
        "required": ["new_perspective_character", "rewritten_scene"]
    }
}

class ToolInjectFourthWallBreak(Tool):
    async def execute(self, **kwargs) -> Response:
        character = self.args.get("character", kwargs.get("character"))
        target_line = self.args.get("target_line", kwargs.get("target_line", ""))
        meta_commentary = self.args.get("meta_commentary", kwargs.get("meta_commentary"))
        return Response(message=f"[{character} turns to the camera during '{target_line}']: {meta_commentary}", break_loop=False)

class ToolFormatActionSequence(Tool):
    async def execute(self, **kwargs) -> Response:
        characters = self.args.get("characters_involved", kwargs.get("characters_involved", []))
        beats = self.args.get("action_beats", kwargs.get("action_beats", []))
        pacing = self.args.get("pacing_notes", kwargs.get("pacing_notes", ""))

        output = f"ACTION SEQUENCE with {', '.join(characters)}:\n"
        for beat in beats:
            output += f"- {beat}\n"
        output += f"Pacing: {pacing}"
        return Response(message=output, break_loop=False)

class ToolGenerateCharacterMotivation(Tool):
    async def execute(self, **kwargs) -> Response:
        character = self.args.get("character", kwargs.get("character"))
        action = self.args.get("action", kwargs.get("action"))
        tarot = self.args.get("tarot_archetype", kwargs.get("tarot_archetype", "The Fool"))
        hidden = self.args.get("hidden_motivation", kwargs.get("hidden_motivation"))

        output = f"MOTIVATION for {character} doing {action}:\n"
        output += f"Tarot: {tarot}\n"
        output += f"Hidden Truth: {hidden}"
        return Response(message=output, break_loop=False)

class ToolEscalateTension(Tool):
    async def execute(self, **kwargs) -> Response:
        stakes = self.args.get("current_stakes", kwargs.get("current_stakes", "Low"))
        new_stakes = self.args.get("new_stakes", kwargs.get("new_stakes"))
        turning = self.args.get("turning_point", kwargs.get("turning_point"))

        output = f"TENSION ESCALATED from {stakes} to {new_stakes} at {turning}."
        return Response(message=output, break_loop=False)

class ToolWriteDialogue(Tool):
    async def execute(self, **kwargs) -> Response:
        char1 = self.args.get("character1", kwargs.get("character1"))
        char2 = self.args.get("character2", kwargs.get("character2", ""))
        dialogue = self.args.get("dialogue_snippet", kwargs.get("dialogue_snippet"))

        chars = char1 if not char2 else f"{char1} and {char2}"
        return Response(message=f"DIALOGUE ({chars}):\n{dialogue}", break_loop=False)

class ToolOptimizePacing(Tool):
    async def execute(self, **kwargs) -> Response:
        scene = self.args.get("scene_text", kwargs.get("scene_text"))
        opts = self.args.get("optimizations", kwargs.get("optimizations"))

        return Response(message=f"PACING OPTIMIZED:\n{opts}\n\nFor scene:\n{scene}", break_loop=False)

class ToolWeaveBackstory(Tool):
    async def execute(self, **kwargs) -> Response:
        character = self.args.get("character", kwargs.get("character"))
        backstory = self.args.get("backstory_element", kwargs.get("backstory_element"))

        return Response(message=f"BACKSTORY WEAVED for {character}: {backstory}", break_loop=False)

class ToolWriteClimax(Tool):
    async def execute(self, **kwargs) -> Response:
        build_up = self.args.get("build_up", kwargs.get("build_up", ""))
        climax = self.args.get("climax_event", kwargs.get("climax_event"))

        return Response(message=f"CLIMAX:\nBuild-up: {build_up}\nEvent: {climax}", break_loop=False)



class ToolGeneratePlotTwist(Tool):
    async def execute(self, **kwargs) -> Response:
        scenario = self.args.get("current_scenario", kwargs.get("current_scenario", ""))
        twist_type = self.args.get("twist_type", kwargs.get("twist_type", "Unexpected"))
        twist = self.args.get("twist_description", kwargs.get("twist_description", ""))

        output = f"PLOT TWIST ({twist_type}):\n{twist}\n\nImpacts scenario: {scenario}"
        return Response(message=output, break_loop=False)

class ToolRewriteFromPerspective(Tool):
    async def execute(self, **kwargs) -> Response:
        char = self.args.get("new_perspective_character", kwargs.get("new_perspective_character", ""))
        rewrite = self.args.get("rewritten_scene", kwargs.get("rewritten_scene", ""))

        output = f"PERSPECTIVE SHIFT ({char}):\n{rewrite}"
        return Response(message=output, break_loop=False)

class ScriptOrchestrator(Tool):
    """
    Tool for Aria to orchestrate the writing of a script through the Writers' Room.
    """
    def __init__(self, agent: Agent, name="script_orchestrator", method=None, args=None, message="", loop_data=None, **kwargs):
        super().__init__(agent, name, method, args or {}, message, loop_data, **kwargs)
        self.config_path = "conf/writers_room_config.json"

    async def execute(self, **kwargs) -> Response:
        initial_script = self.args.get("initial_script", kwargs.get("initial_script", ""))
        if not initial_script:
             return Response(message="Error: initial_script is required.", break_loop=False)

        try:
            with open(self.config_path, 'r') as file:
                config = json.load(file)
            orchestrator = config['writers_room']['orchestrator']
            agents = config['writers_room']['subordinates']
        except Exception as e:
            return Response(message=f"Error loading writers room config: {e}", break_loop=False)

        # Build execution trace string
        trace = []
        trace.append(f"Aria is initiating the {orchestrator['role']} sequence...")

        current_script_state = initial_script

        for writer in agents:
            trace.append(f"Passing the baton to: {writer['name']}...")
            # For this tool implementation, we will append a simulated completion
            # In a full implementation, you'd spawn/call a sub-agent with writer['system_prompt']
            current_script_state += f"\n\n[Processed by {writer['name']}]\n"
            current_script_state += f"Applied tools: {', '.join(writer['tools_allowed'])}"

        trace.append("Aria has received the final script back. Execution complete.")

        # Combine trace and final script
        output = "\n".join(trace) + "\n\n=== FINAL SCRIPT STATE ===\n" + current_script_state

        return Response(message=output, break_loop=False)
