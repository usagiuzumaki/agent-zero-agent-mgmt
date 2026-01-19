### screenwriting_pipeline:
- Orchestrates a full screenwriting production line including analysis, brainstorming, drafting, dialogue evaluation, formatting, and optional specialized analysis.
- Use with `task` (the writing task description) and `project_name`.
- Optional flags:
    - `include_world_building`: Generate world setting/lore.
    - `include_character_analysis`: Analyze/Generate characters.
    - `include_pacing`: Analyze pacing metrics.
    - `include_emotional_tension`: Analyze emotional tension.
    - `include_marketability`: Evaluate market potential.
    - `include_mbti`: Evaluate character personalities (MBTI).
    - `include_scream_analysis`: Analyze scream intensity.
    - `include_storyboard`: Generate visual storyboard prompts.

**Example usage**:
~~~json
{
    "thoughts": ["I will run the screenwriting pipeline with full analysis."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a horror scene in a haunted cabin.",
        "project_name": "Ghost Story",
        "include_pacing": true,
        "include_emotional_tension": true,
        "include_scream_analysis": true,
        "include_storyboard": true
    }
}
~~~
