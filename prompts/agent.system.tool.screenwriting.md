### screenwriting:
Tool for managing screenwriting data and features (CRUD).
Operations: view, add_character, add_quote, add_scene, add_sketch, create_project, update_outline, search_quotes, ingest_storybook.
Data types for view: all, book_outline, story_bible, character_profiles, sick_quotes, sketches_imagery, storybook.
- Use `operation: view` with `data_type` (all, book_outline, story_bible, character_profiles, sick_quotes, sketches_imagery, storybook) to view data.
- Use `operation: add_character` with `name`, `role`, `backstory`, `personality`, `goals`, `conflicts`, `arc`, `appearance` to add a character.
- Use `operation: add_quote` with `quote`, `character`, `context`, `category` to add a quote.
- Use `operation: add_scene` with `title`, `description`, `setting`, `characters`, `conflict`, `resolution`, `chapter`, `act` to add a scene.
- Use `operation: add_sketch` with `title`, `description`, `type`, `image_url`, `characters`, `scene`, `mood` to add a sketch.
- Use `operation: create_project` with `name`, `genre`, `logline` to create a project.
- Use `operation: update_outline` with `title`, `genre`, `logline`, `acts`, `chapters`, `plot_points` to update the outline.
- Use `operation: ingest_storybook` with `name`, `content`, `description`, `tags` to add a document to the Storybook.
- Use `operation: search_quotes` with `search` to find quotes.

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
