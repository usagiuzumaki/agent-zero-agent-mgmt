### screenwriting_specialist:
- Consults a specific screenwriting specialist agent for a focused task.
- Use `specialist` to select the agent (PlotAnalyzer, CreativeIdeas, CoWriter, DialogueEvaluator, ScriptFormatter, CharacterAnalyzer, PacingMetrics, EmotionalTension, Marketability, MBTIEvaluator, ScreamAnalyzer, StoryboardGenerator, WorldBuilder).
- Use `task` to describe the work needed.

**Example usage**:
~~~json
{
    "thoughts": ["I need to brainstorm plot twists."],
    "tool_name": "screenwriting_specialist",
    "tool_args": {
        "specialist": "CreativeIdeas",
        "task": "Brainstorm 5 plot twists for a mystery thriller."
    }
}
~~~
