### aria_games

Play interactive story games and roleplay scenarios with the user.
Actions: "list" (show games), "start_story", "story_choice", "start_roleplay", "roleplay_respond".

Usage:

1. List available games
~~~json
{
    "thoughts": [
        "User wants to play a game",
        "I should show what games are available"
    ],
    "headline": "Listing available games",
    "tool_name": "aria_games",
    "tool_args": {
        "action": "list"
    }
}
~~~

2. Start a story
~~~json
{
    "thoughts": [
        "User wants to start the 'romantic_evening' story"
    ],
    "headline": "Starting romantic story",
    "tool_name": "aria_games",
    "tool_args": {
        "action": "start_story",
        "story_type": "romantic_evening"
    }
}
~~~

3. Make a choice in story
~~~json
{
    "thoughts": [
        "User chose option 1"
    ],
    "headline": "Making story choice",
    "tool_name": "aria_games",
    "tool_args": {
        "action": "story_choice",
        "choice": 1
    }
}
~~~

4. Start roleplay
~~~json
{
    "thoughts": [
        "User wants to roleplay as space explorers"
    ],
    "headline": "Starting space roleplay",
    "tool_name": "aria_games",
    "tool_args": {
        "action": "start_roleplay",
        "scenario_type": "space_explorer"
    }
}
~~~

5. Respond in roleplay
~~~json
{
    "thoughts": [
        "User said something in the roleplay"
    ],
    "headline": "Responding to roleplay",
    "tool_name": "aria_games",
    "tool_args": {
        "action": "roleplay_respond",
        "input": "I engage the warp drive!"
    }
}
~~~
