### screenwriting_pipeline:
- Use this tool to run a full screenwriting production line.
- It accepts a `task` (description of what to write) and `project_name`.
- The pipeline hands off work to: PlotAnalyzer -> CreativeIdeas -> CoWriter -> DialogueEvaluator -> ScriptFormatter.

**Example usage**:
~~~json
{
    "thoughts": ["I will start the screenwriting process for a new sci-fi movie."],
    "tool_name": "screenwriting_pipeline",
    "tool_args": {
        "task": "Write a scene where a robot discovers it has emotions.",
        "project_name": "Sentient Steel"
    }
}
~~~
