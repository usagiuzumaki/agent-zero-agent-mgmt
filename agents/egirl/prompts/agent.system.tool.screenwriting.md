### screenwriting:
- Use this tool to manage screenwriting data (characters, scenes, quotes, outline).
- Arguments: `operation` and `data_type` (for 'view') or other specific args.
- Operations: `view`, `add_character`, `add_quote`, `add_scene`, `add_sketch`, `create_project`, `update_outline`, `search_quotes`, `ingest_storybook`.

**Example usage**:
~~~json
{
    "thoughts": ["I need to add a new character."],
    "tool_name": "screenwriting",
    "tool_args": {
        "operation": "add_character",
        "name": "John Doe",
        "role": "Protagonist",
        "backstory": "A former cop..."
    }
}
~~~
