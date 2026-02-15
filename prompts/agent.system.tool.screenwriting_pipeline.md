### screenwriting_pipeline:
Orchestrates a screenwriting pipeline by handing off tasks to specialized agents.
Supported flags: include_world_building, include_character_analysis, include_pacing, include_tension, include_marketability, include_mbti, include_scream, include_storyboard.
- Orchestrates a complete screenwriting production line using specialized agents.
- Use `task` to describe the overall goal.
- Use `project_name` to identify the project.
- Optional boolean flags to enable specific stages:
    - `include_world_building`: World Builder (Setting/Lore)
    - `include_character_analysis`: Character Analyzer
    - `include_pacing`: Pacing Metrics
    - `include_tension`: Emotional Tension
    - `include_marketability`: Marketability Assessment
    - `include_mbti`: MBTI Evaluator
    - `include_scream`: Scream/Intensity Analyzer
    - `include_storyboard`: Storyboard Generator

**Example usage**:
~~~json
{
    "thoughts": ["I want to write a sci-fi movie about AI."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a screenplay about an AI that learns to love.",
        "project_name": "AI Love Story",
        "include_world_building": true,
        "include_character_analysis": true
    }
}
~~~
