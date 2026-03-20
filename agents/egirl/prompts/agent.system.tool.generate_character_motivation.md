### GenerateCharacterMotivation
Generate deep psychological and mystical motivation for a character's actions.

**Usage:**
```json
{
  "thoughts": ["why I am using this tool"],
  "tool_name": "generate_character_motivation",
  "tool_args": {
    "character": "Jules",
    "action": "Hack the mainframe",
    "tarot_archetype": "The Magician",
    "hidden_motivation": "To find the lost source code."
  }
}
```

**Arguments:**
- `character` (string, required): The character's name.
- `action` (string, required): The action to motivate.
- `tarot_archetype` (string, optional): The archetype driving them.
- `hidden_motivation` (string, required): The hidden motivation.

**Returns:** The processed text from the tool.
