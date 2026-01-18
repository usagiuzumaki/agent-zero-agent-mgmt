### screenwriting_pipeline:
- Orchestrates a full screenwriting production line including analysis, brainstorming, drafting, dialogue evaluation, and formatting.
- Can optionally include advanced analysis tools (pacing, marketability, emotional tension, etc.).
- Use with `task` (the writing task description) and `project_name`.

**Example usage**:
~~~json
{
    "thoughts": ["I will start the screenwriting process for the new sci-fi project and analyze its marketability."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a scene where the hero discovers the alien artifact.",
        "project_name": "Project Alpha",
        "include_world_building": true,
        "include_marketability": true,
        "include_pacing": true
    }
}
~~~
