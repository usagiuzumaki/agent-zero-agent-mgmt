### screenwriting:
Tool for managing screenwriting data and features (CRUD).
Operations: view, add_character, add_quote, add_scene, add_sketch, create_project, update_outline, search_quotes, ingest_storybook.
Data types for view: all, book_outline, story_bible, character_profiles, sick_quotes, sketches_imagery, storybook.

**Example usage**:
~~~json
{
    "thoughts": [
        "I need to add a new character."
    ],
    "headline": "Adding a new character",
    "tool_name": "screenwriting",
    "tool_args": {
        "operation": "add_character",
        "name": "John Doe",
        "role": "Protagonist",
        "backstory": "..."
    }
}
~~~
