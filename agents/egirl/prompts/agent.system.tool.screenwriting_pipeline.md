### screenwriting_pipeline:
- Orchestrates a full screenwriting production line including analysis, brainstorming, drafting, dialogue evaluation, formatting, and optional post-analysis.
- Use with `task` (the writing task description) and `project_name`.
- Optional boolean flags:
    - `include_world_building` (Generate setting/lore first)
    - `include_character_analysis` (Analyze/Generate characters first)
    - `include_pacing` (Pacing metrics analysis)
    - `include_emotional_tension` (Emotional tension analysis)
    - `include_mbti_evaluator` (Character personality evaluation)
    - `include_scream_analysis` (Scream/Intensity analysis)
    - `include_marketability` (Market potential assessment)
    - `include_storyboard_generator` (Visual storyboard generation)

**Example usage**:
~~~json
{
    "thoughts": ["I will start the screenwriting process for the new sci-fi project with full analysis."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a scene where the hero discovers the alien artifact.",
        "project_name": "Project Alpha",
        "include_world_building": true,
        "include_character_analysis": true,
        "include_pacing": true,
        "include_emotional_tension": true,
        "include_marketability": true
    }
}
~~~
