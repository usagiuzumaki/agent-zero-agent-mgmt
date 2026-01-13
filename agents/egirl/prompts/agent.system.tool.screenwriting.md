# Screenwriting Database Tool

Use this tool to view, add, or search screenwriting data such as characters, quotes, scenes, sketches, and project outlines.

## Arguments:
- `operation`: The operation to perform. Options:
    - `'view'`: View data (requires `data_type`).
    - `'add_character'`: Add a new character profile.
    - `'add_quote'`: Save a memorable quote.
    - `'add_scene'`: Add a scene card.
    - `'add_sketch'`: Add a visual sketch/idea.
    - `'create_project'`: Initialize a new project.
    - `'update_outline'`: Update the book/script outline.
    - `'search_quotes'`: Search saved quotes.
    - `'ingest_storybook'`: Ingest a document into the storybook.
- `data_type` (for 'view'): `'all'`, `'character_profiles'`, `'sick_quotes'`, `'book_outline'`, `'story_bible'`, `'sketches_imagery'`, `'storybook'`.

## Additional Arguments per Operation:
- **add_character**: `name`, `role`, `backstory`, `personality`, `goals`, `conflicts`, `arc`, `appearance`.
- **add_quote**: `quote`, `character`, `context`, `category`.
- **add_scene**: `title`, `description`, `setting`, `characters` (list), `conflict`, `resolution`, `chapter`, `act`.
- **add_sketch**: `title`, `description`, `type` (default 'sketch'), `image_url`, `characters`, `scene`, `mood`, `colors`.
- **create_project**: `name`, `genre`, `logline`.
- **update_outline**: `title`, `genre`, `logline`, `acts` (list), `chapters` (list), `plot_points` (list).
- **ingest_storybook**: `name`, `content`, `description`, `tags` (list).
- **search_quotes**: `search` (term).
