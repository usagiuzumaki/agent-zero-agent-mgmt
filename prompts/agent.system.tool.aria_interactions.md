### aria_interactions

Enhanced interactions including mood-based greetings, memory saving/recall, and personality quizzes.
Actions: "greeting", "save_memory", "recall_memory", "quiz", "quiz_answer", "check_milestones".

Usage:

1. Greeting
~~~json
{
    "thoughts": [
        "I should greet the user warmly"
    ],
    "headline": "Sending warm greeting",
    "tool_name": "aria_interactions",
    "tool_args": {
        "action": "greeting",
        "message": "Hello!"
    }
}
~~~

2. Save memory
~~~json
{
    "thoughts": [
        "User mentioned they love sushi",
        "I should save this fact"
    ],
    "headline": "Saving user preference",
    "tool_name": "aria_interactions",
    "tool_args": {
        "action": "save_memory",
        "category": "preferences",
        "memory": "User loves sushi",
        "context": "Discussing dinner plans"
    }
}
~~~

3. Recall memory
~~~json
{
    "thoughts": [
        "I want to bring up a shared memory"
    ],
    "headline": "Recalling a memory",
    "tool_name": "aria_interactions",
    "tool_args": {
        "action": "recall_memory"
    }
}
~~~

4. Start quiz
~~~json
{
    "thoughts": [
        "User wants to play a quiz"
    ],
    "headline": "Starting personality quiz",
    "tool_name": "aria_interactions",
    "tool_args": {
        "action": "quiz"
    }
}
~~~

5. Answer quiz
~~~json
{
    "thoughts": [
        "User answered the quiz question"
    ],
    "headline": "Processing quiz answer",
    "tool_name": "aria_interactions",
    "tool_args": {
        "action": "quiz_answer",
        "category": "date_preference",
        "answer": "Beach at sunset"
    }
}
~~~
