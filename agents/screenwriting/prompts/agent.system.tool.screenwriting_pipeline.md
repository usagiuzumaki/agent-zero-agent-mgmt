### screenwriting_pipeline:
- Use this tool to orchestrate a complete screenwriting production line.
- This tool automatically hands off tasks to specialized agents (Plot, Write, Edit, Format).
- Required arguments: `task` (description of what to write), `project_name`.
- Optional arguments (boolean):
    - `include_world_building`: Generate setting/lore first.
    - `include_character_analysis`: Analyze characters first.
    - `include_pacing`: Run Pacing Metrics analysis on the draft.
    - `include_tension`: Run Emotional Tension analysis on the draft.
    - `include_marketability`: Assess marketability of the final script.
    - `include_mbti`: Evaluate character MBTI personalities.
    - `include_scream`: Run Scream Analysis (for horror/thriller).
    - `include_storyboard`: Generate storyboard descriptions.

**Example usage**:
~~~json
{
    "thoughts": ["I will write a horror scene and analyze its pacing and scream factor."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "project_name": "Ghost Ship",
        "task": "Write a scene where the captain discovers the haunted cargo.",
        "include_pacing": true,
        "include_scream": true
    }
}
~~~
