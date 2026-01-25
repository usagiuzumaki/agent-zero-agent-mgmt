### screenwriting_pipeline:
Orchestrates a screenwriting pipeline by handing off tasks to specialized agents.
Supported flags: include_world_building, include_character_analysis, include_pacing, include_tension, include_marketability, include_mbti, include_scream, include_storyboard.

**Example usage**:
~~~json
{
    "thoughts": [
        "I need to write a script about...",
        "I should include character analysis and pacing metrics."
    ],
    "headline": "Starting screenwriting pipeline",
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a sci-fi thriller about...",
        "project_name": "Project Alpha",
        "include_character_analysis": "true",
        "include_pacing": "true"
    }
}
~~~
