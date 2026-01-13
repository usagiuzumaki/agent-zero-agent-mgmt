### screenwriting_pipeline:
- Orchestrates a full screenwriting production line including analysis, brainstorming, drafting, dialogue evaluation, and formatting.
- Use with `task` (the writing task description) and `project_name`.

**Example usage**:
~~~json
{
    "thoughts": ["I will start the screenwriting process for the new sci-fi project."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a scene where the hero discovers the alien artifact.",
        "project_name": "Project Alpha"
    }
}
~~~
