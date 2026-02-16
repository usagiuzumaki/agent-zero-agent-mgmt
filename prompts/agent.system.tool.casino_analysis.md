### casino_analysis

Evaluates poker hands and scenarios to provide the raw probability data required for a Fate Report.
Args:
- `cards`: List of strings representing cards (e.g., ["As", "Kd", "Qc", "Jh", "Th"]). First two are hole cards, others are board.
- `scenario`: A description of the life decision or game situation being analyzed.

Usage:
~~~json
{
    "thoughts": [
        "The user is asking about a difficult career choice, comparing it to an all-in play with a mediocre hand.",
        "I will evaluate the metaphorical hand to provide a baseline for my Fate Report."
    ],
    "headline": "Evaluating the odds of destiny",
    "tool_name": "casino_analysis",
    "tool_args": {
        "cards": ["Js", "Ts", "8s", "7s", "2s"],
        "scenario": "Deciding whether to quit the stable job for the startup gamble."
    }
}
~~~
