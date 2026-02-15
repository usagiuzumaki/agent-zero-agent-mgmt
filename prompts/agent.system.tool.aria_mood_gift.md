### aria_mood_gift

Generate mood-based images or virtual gifts for the user.
Actions: "mood_image", "gift".

Usage:

1. Generate mood image
~~~json
{
    "thoughts": [
        "I want to show my current mood with an image"
    ],
    "headline": "Generating mood image",
    "tool_name": "aria_mood_gift",
    "tool_args": {
        "action": "mood_image"
    }
}
~~~

2. Give a gift
~~~json
{
    "thoughts": [
        "I want to give the user a virtual gift"
    ],
    "headline": "Giving virtual gift",
    "tool_name": "aria_mood_gift",
    "tool_args": {
        "action": "gift"
    }
}
~~~
