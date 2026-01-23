### screenwriting_specialist:
Directly consult a specialized screenwriting agent for a specific task.
- `specialist` (string): The name of the specialist agent. Options: PlotAnalyzer, CreativeIdeas, CoWriter, DialogueEvaluator, ScriptFormatter, CharacterAnalyzer, PacingMetrics, EmotionalTension, Marketability, MBTIEvaluator, ScreamAnalyzer, StoryboardGenerator, WorldBuilder.
- `task` (string): The specific task for the specialist.

**Example usage**:
~~~json
{
    "thoughts": ["I want to analyze the pacing of this specific scene."],
    "tool_name": "screenwriting_specialist",
    "tool_args": {
        "specialist": "PacingMetrics",
        "task": "Analyze the pacing of the following text: ..."
    }
}
~~~
