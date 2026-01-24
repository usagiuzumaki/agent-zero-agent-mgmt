### screenwriting_pipeline

Orchestrate a complete screenwriting production line.
Pass a task description and project name.
Enable specific stages as needed (world building, character analysis, etc).

usage:

~~~json
{
    "thoughts": [
        "I need to write a full screenplay draft for a sci-fi movie.",
        "I will enable world building and character analysis."
    ],
    "headline": "Starting screenwriting pipeline",
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a story about a robot who wants to be a chef.",
        "project_name": "The Iron Chef",
        "include_world_building": true,
        "include_character_analysis": true,
        "include_pacing": true,
        "include_marketability": true
    }
}
~~~
