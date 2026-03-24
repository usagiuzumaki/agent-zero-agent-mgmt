### EscalateTension
Escalate the dramatic tension in preparation for the climax.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "escalate_tension",
  "tool_args": {
    "current_stakes": "Getting fired",
    "new_stakes": "Losing everything",
    "turning_point": "When the boss walks in"
  }
}
```

**Arguments:**
- `current_stakes` (string, optional): Current stakes in the scene.
- `new_stakes` (string, required): The escalated stakes.
- `turning_point` (string, required): The beat where tension escalates.

**Returns:** The processed text from the tool.
