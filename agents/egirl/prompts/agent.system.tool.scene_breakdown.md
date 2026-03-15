### SceneBreakdown
Breaks a prompt or outline into scenes.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "scene_breakdown",
  "tool_args": {
    "prompt": "value"
  }
}
```

**Arguments:**
- `context` (string, required): The prompt or outline to break into scenes.

**Returns:** The processed text from the tool.
