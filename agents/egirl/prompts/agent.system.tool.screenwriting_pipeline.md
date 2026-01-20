### screenwriting_pipeline:
- Orchestrates a full screenwriting production line including analysis, brainstorming, drafting, dialogue evaluation, and formatting.
- Optional stages: World Building, Character Analysis, Pacing Metrics, Emotional Tension, Marketability, MBTI Evaluation, Scream Analysis, Storyboard Generation.
- Use with `task` (the writing task description) and `project_name`.
- Optional flags: `include_world_building`, `include_character_analysis`, `include_pacing`, `include_tension`, `include_marketability`, `include_mbti`, `include_scream`, `include_storyboard`.

**Example usage**:
~~~json
{
    "thoughts": ["I will start the screenwriting process for the new sci-fi project with full analysis."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a scene where the hero discovers the alien artifact.",
        "project_name": "Project Alpha",
        "include_world_building": true,
        "include_pacing": true,
        "include_marketability": true
    }
}
~~~
