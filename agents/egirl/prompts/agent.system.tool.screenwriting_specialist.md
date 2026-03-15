### ScreenwritingSpecialist
Smart router for screenwriting tools, handles pipeline or direct mode.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "screenwriting_specialist",
  "tool_args": {
        "prompt": "value",
    "mode": "direct",
    "tool_name": "CharacterAnalyzer"
  }
}
```

**Arguments:**
- `prompt` (string, required): The screenwriting prompt.
- `mode` (string, optional): 'pipeline' or 'direct'.
- `tool_name` (string, optional): The specific tool to invoke in 'direct' mode (e.g. 'CharacterAnalyzer').

**Returns:** The processed text from the tool.
