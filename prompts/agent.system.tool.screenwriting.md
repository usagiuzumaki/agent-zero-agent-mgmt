### screenwriting

Manage screenwriting data and features (Bible, Characters, Scenes, etc).
Operations:
- view: View data (args: data_type='all'|'book_outline'|'story_bible'|'character_profiles'|'sick_quotes'|'sketches_imagery'|'storybook')
- add_character: Add a character (args: name, role, etc)
- add_quote: Add a quote (args: quote, character, context)
- add_scene: Add a scene (args: title, description, etc)
- add_sketch: Add a sketch (args: title, description, etc)
- create_project: Create a new project (args: name, genre, logline)
- update_outline: Update outline (args: title, acts, chapters)
- search_quotes: Search quotes (args: search)
- ingest_storybook: Ingest text into storybook (args: name, content, description)

usage:

~~~json
{
    "thoughts": [
        "I need to view the current character profiles."
    ],
    "headline": "Viewing character profiles",
    "tool_name": "screenwriting",
    "tool_args": {
        "operation": "view",
        "data_type": "character_profiles"
    }
}
~~~
