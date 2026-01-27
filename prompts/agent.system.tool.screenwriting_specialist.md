### screenwriting_specialist:
Allows direct access to specialized screenwriting agents for specific tasks.
Available Specialists: PlotAnalyzer, CreativeIdeas, CoWriter, DialogueEvaluator, ScriptFormatter, CharacterAnalyzer, PacingMetrics, EmotionalTension, Marketability, MBTIEvaluator, ScreamAnalyzer, StoryboardGenerator, WorldBuilder, VersionTracker.
- Consults a specific screenwriting specialist agent for a focused task.
- Use `specialist` to select the agent (PlotAnalyzer, CreativeIdeas, CoWriter, DialogueEvaluator, ScriptFormatter, CharacterAnalyzer, PacingMetrics, EmotionalTension, Marketability, MBTIEvaluator, ScreamAnalyzer, StoryboardGenerator, WorldBuilder, VersionTracker).
- Use `task` to describe the work needed.

**Example usage**:
~~~json
{
    "thoughts": [
        "I need to analyze the plot structure of this draft."
    ],
    "headline": "Consulting Plot Analyzer",
    "tool_name": "screenwriting_specialist",
    "tool_args": {
        "specialist": "PlotAnalyzer",
        "task": "Analyze the following plot summary..."
        
    "thoughts": ["I need to brainstorm plot twists."],
    "tool_name": "screenwriting_specialist",
    "tool_args": {
        "specialist": "CreativeIdeas",
        "task": "Brainstorm 5 plot twists for a mystery thriller."
    }
}
~~~
