### call_subordinate:
You can use subordinates for subtasks. Subordinates are specialized agents with their own prompts.
Message field: always describe role, task details goal overview for new subordinate.
Delegate specific subtasks not entire task.
Make sure to verify subordinate results.

Available prompt profiles:
{{agent_profiles}}

Reset arg usage:
  "true": spawn new subordinate
  "false": continue existing subordinate

Example usage:
~~~json
{
    "thoughts": [
        "The result seems to be ok but...",
        "I will ask a coder subordinate to fix...",
    ],
    "tool_name": "call_subordinate",
    "tool_args": {
        "message": "Instructions for the subordinate",
        "reset": "true",
        "profile": "default"
    }
}
~~~
