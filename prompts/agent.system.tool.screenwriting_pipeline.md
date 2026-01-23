### screenwriting_pipeline:
Orchestrates a comprehensive screenwriting pipeline, handing tasks down through specialized agents (World Builder, Character Analyzer, Plot Analyzer, Creative Ideas, Co-Writer, Dialogue Evaluator, etc.).
- `task` (string): The writing task description.
- `project_name` (string): The name of the project.
- `include_world_building` (bool): Include world building step?
- `include_character_analysis` (bool): Include character analysis step?
- `include_pacing` (bool): Include pacing metrics analysis?
- `include_tension` (bool): Include emotional tension analysis?
- `include_marketability` (bool): Include marketability assessment?
- `include_mbti` (bool): Include MBTI personality evaluation?
- `include_scream` (bool): Include scream/intensity analysis?
- `include_storyboard` (bool): Include storyboard generation?

**Example usage**:
~~~json
{
    "thoughts": ["I need to develop a full sci-fi script concept with character analysis and tension tracking."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a scene where the protagonist discovers the alien artifact.",
        "project_name": "Project Nebula",
        "include_world_building": true,
        "include_character_analysis": true,
        "include_tension": true
    }
}
~~~
