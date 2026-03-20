### RewriteFromPerspective
Rewrite a scene from an entirely different, unexpected character's point of view.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "rewrite_from_perspective",
  "tool_args": {
    "scene_text": "The hero enters the room.",
    "new_perspective_character": "The toaster",
    "rewritten_scene": "The toaster watched the man enter."
  }
}
```

**Arguments:**
- `scene_text` (string, optional): The original scene.
- `new_perspective_character` (string, required): The unexpected character POV.
- `rewritten_scene` (string, required): The rewritten scene content.

**Returns:** The processed text from the tool.
