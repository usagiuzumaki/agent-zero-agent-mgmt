### DialoguePolisher
Refines all dialogue.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "dialogue_polisher",
  "tool_args": {
    "context": "value"
  }
}
```

**Arguments:**
- `context` (string, required): The scene draft with dialogue to polish.

**Returns:** The processed text from the tool.
