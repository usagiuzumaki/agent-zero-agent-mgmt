### InjectFourthWallBreak
Inject a meta-humorous fourth wall break into the scene.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "inject_fourth_wall_break",
  "tool_args": {
    "character": "Jules",
    "target_line": "Some line",
    "meta_commentary": "I can't believe I have to say this line."
  }
}
```

**Arguments:**
- `character` (string, required): The character breaking the fourth wall.
- `target_line` (string, optional): The line or beat to interject on.
- `meta_commentary` (string, required): The meta-humor commentary to insert.

**Returns:** The processed text from the tool.
