### `screenwriting`

Use this tool to manage screenwriting data and features, such as characters, scenes, quotes, sketches, and outlines.

Arguments:
- `operation` (string, required): The operation to perform. Options: "view", "add_character", "add_quote", "add_scene", "add_sketch", "create_project", "update_outline", "search_quotes", "ingest_storybook".
- `data_type` (string, optional): For "view" operation, specifies data type ("all", "book_outline", "story_bible", "character_profiles", "sick_quotes", "sketches_imagery", "storybook").
- `name` (string): For adding characters or creating projects.
- `role` (string): For adding characters.
- `backstory` (string): For adding characters.
- `personality` (string): For adding characters.
- `quote` (string): For adding quotes.
- `character` (string): For adding quotes (speaker).
- `context` (string): For adding quotes.
- `title` (string): For adding scenes/sketches or updating outline.
- `description` (string): For adding scenes/sketches.
- `setting` (string): For adding scenes.
- `content` (string): For ingesting storybook documents.
- `search` (string): For searching quotes.
- `genre`, `logline`: For projects/outlines.
