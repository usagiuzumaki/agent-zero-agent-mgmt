### ScreenwritingPipeline
Orchestrates the subordinate screenwriting pipeline via a linear handoff chain.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "screenwriting_pipeline",
  "tool_args": {
    "prompt": "value"
  }
}
```

**Arguments:**
- `prompt` (string, required): The initial screenwriting request or idea.

**Returns:** The processed text from the tool.
