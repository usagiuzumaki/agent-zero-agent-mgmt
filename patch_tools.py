import re

with open("python/tools/writers_room.py", "r") as f:
    content = f.read()

# Add schemas
schemas = """
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
"""

content = content.replace("class ToolInjectFourthWallBreak(Tool):", schemas + "\nclass ToolInjectFourthWallBreak(Tool):")

# Add classes
classes = """
class ToolGeneratePlotTwist(Tool):
    async def execute(self, **kwargs) -> Response:
        scenario = self.args.get("current_scenario", kwargs.get("current_scenario", ""))
        twist_type = self.args.get("twist_type", kwargs.get("twist_type", "Unexpected"))
        twist = self.args.get("twist_description", kwargs.get("twist_description", ""))

        output = f"PLOT TWIST ({twist_type}):\\n{twist}\\n\\nImpacts scenario: {scenario}"
        return Response(message=output, break_loop=False)

class ToolRewriteFromPerspective(Tool):
    async def execute(self, **kwargs) -> Response:
        char = self.args.get("new_perspective_character", kwargs.get("new_perspective_character", ""))
        rewrite = self.args.get("rewritten_scene", kwargs.get("rewritten_scene", ""))

        output = f"PERSPECTIVE SHIFT ({char}):\\n{rewrite}"
        return Response(message=output, break_loop=False)
"""

content = content.replace("class ScriptOrchestrator(Tool):", classes + "\nclass ScriptOrchestrator(Tool):")

with open("python/tools/writers_room.py", "w") as f:
    f.write(content)

print("Patch applied.")
