### FormatActionSequence
Format a high-octane action sequence to improve pacing.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "format_action_sequence",
  "tool_args": {
    "characters_involved": ["Jules", "Agent Zero"],
    "action_beats": ["Jules dodges", "Agent Zero counters"],
    "pacing_notes": "Fast and aggressive"
  }
}
```

**Arguments:**
- `characters_involved` (array of strings, optional): Characters in the action.
- `action_beats` (array of strings, optional): Rapid-fire action beats.
- `pacing_notes` (string, optional): Notes on pacing.

**Returns:** The processed text from the tool.
