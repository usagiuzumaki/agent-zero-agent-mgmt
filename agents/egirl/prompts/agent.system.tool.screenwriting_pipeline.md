### screenwriting_pipeline:
- Orchestrates a full screenwriting production line including analysis, brainstorming, drafting, dialogue evaluation, formatting, and optional specialized analysis.
- Use with `task` (the writing task description) and `project_name`.
- Optional flags: `include_world_building`, `include_character_analysis`, `include_pacing`, `include_tension`, `include_marketability`, `include_mbti`, `include_scream`, `include_storyboard` (all booleans).

**Example usage**:
~~~json
{
    "thoughts": ["I will start the screenwriting process for the new sci-fi project, including character analysis and marketability assessment."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a scene where the hero discovers the alien artifact.",
        "project_name": "Project Alpha",
        "include_character_analysis": true,
        "include_marketability": true
    }
}
~~~
