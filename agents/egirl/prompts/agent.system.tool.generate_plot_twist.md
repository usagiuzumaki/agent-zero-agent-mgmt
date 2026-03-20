### GeneratePlotTwist
Generate an unpredictable plot twist.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "generate_plot_twist",
  "tool_args": {
    "current_scenario": "The team is cornered.",
    "twist_type": "Betrayal",
    "twist_description": "The friendly drone turns hostile."
  }
}
```

**Arguments:**
- `current_scenario` (string, optional): Current scenario.
- `twist_type` (string, optional): Type of twist.
- `twist_description` (string, required): The twist description.

**Returns:** The processed text from the tool.
