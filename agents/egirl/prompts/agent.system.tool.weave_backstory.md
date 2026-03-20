### WeaveBackstory
Weave a character's backstory into the current scene.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "weave_backstory",
  "tool_args": {
    "character": "Jules",
    "backstory_element": "Used to be a rogue AI."
  }
}
```

**Arguments:**
- `character` (string, required): The character's name.
- `backstory_element` (string, required): The backstory to weave in.

**Returns:** The processed text from the tool.
