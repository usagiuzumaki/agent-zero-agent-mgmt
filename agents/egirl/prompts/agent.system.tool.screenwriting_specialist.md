### screenwriting_specialist:
- Consult a specific screenwriting specialist agent for a targeted task.
- Available specialists: `PlotAnalyzer`, `CreativeIdeas`, `CoWriter`, `DialogueEvaluator`, `ScriptFormatter`, `CharacterAnalyzer`, `PacingMetrics`, `EmotionalTension`, `Marketability`, `MBTIEvaluator`, `ScreamAnalyzer`, `StoryboardGenerator`, `WorldBuilder`.
- Use with `specialist` (name) and `task` (description).

**Example usage**:
~~~json
{
    "thoughts": ["I need to analyze the pacing of this scene."],
    "tool_name": "screenwriting_specialist",
    "tool_args": {
        "specialist": "PacingMetrics",
        "task": "Analyze the pacing of the chase scene in Act 2."
    }
}
~~~
