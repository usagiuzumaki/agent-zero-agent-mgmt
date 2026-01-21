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
    "thoughts": ["I will run the screenwriting pipeline with full analysis."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a horror scene in a haunted cabin.",
        "project_name": "Ghost Story",
        "include_pacing": true,
        "include_emotional_tension": true,
        "include_scream_analysis": true,
        "include_storyboard": true
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
