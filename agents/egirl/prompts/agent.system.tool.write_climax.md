### WriteClimax
Write the climax of a scene or act.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "write_climax",
  "tool_args": {
    "build_up": "They run out of ammo.",
    "climax_event": "Jules uses the last EMP grenade."
  }
}
```

**Arguments:**
- `build_up` (string, optional): The build up leading to the climax.
- `climax_event` (string, required): The main event of the climax.

**Returns:** The processed text from the tool.
