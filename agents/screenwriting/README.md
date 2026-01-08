# Screenwriting Agents — Tool Specifications

Each of these tools follows the Agent Zero style:

```json
{
  "tool_name": "story_architect",
  "tool_args": { "...": "..." }
}
```

You can route each tool to a sub-agent whose `system` prompt is the corresponding file in `prompts/`.

---

### Story Architect

**Purpose:** Generate robust structural spines and beat sheets for a story.

**Usage:**
```json
{
  "tool_name": "story_architect",
  "tool_args": {
    "premise": "A disillusioned tarot reader discovers her predictions are starting to literally reshape reality.",
    "genre": "dark fantasy drama",
    "format": "feature",
    "target_runtime_minutes": 110,
    "structure_model": "three_act"
  }
}
```

---

### Character Alchemist

**Purpose:** Forge deep, psychologically rich character bibles and arcs.

**Usage:**
```json
{
  "tool_name": "character_alchemist",
  "tool_args": {
    "name": "Azazel",
    "story_role": "protagonist",
    "initial_concept": "a gifted but emotionally avoidant hacker-prophet",
    "relationships": ["mother: estranged genius", "love_interest: chaotic optimist"],
    "theme": "whether broken people can be worthy of saving the world"
  }
}
```

---

### Dialogue Demon

**Purpose:** Write sharp, subtext-heavy dialogue for a given scene objective.

**Usage:**
```json
{
  "tool_name": "dialogue_demon",
  "tool_args": {
    "scene_purpose": "Azazel finally confronts Tinka about hiding the truth about Gaia's collapse.",
    "characters": [
      {"name": "Azazel", "personality": "guarded, clever, avoids vulnerability"},
      {"name": "Tinka", "personality": "earnest, stubborn, hides guilt with jokes"}
    ],
    "setting": "abandoned subway platform lit by flickering emergency lights",
    "emotional_context": "betrayal, fear of losing each other, looming external threat",
    "existing_beats": [
      "Azazel accuses Tinka of lying",
      "Tinka explains her reasons but doesn't fully confess",
      "They decide to stay together anyway, but trust is shaken"
    ]
  }
}
```

---

### Emotion Cartographer

**Purpose:** Map the emotional arc of a sequence or entire story.

**Usage:**
```json
{
  "tool_name": "emotion_cartographer",
  "tool_args": {
    "scene_list": [
      "01: Azazel alone in his cluttered apartment",
      "02: First glitch in reality during a reading",
      "03: Client returns terrified about a fulfilled prophecy"
    ],
    "protagonist": "Azazel, hyper-aware but emotionally repressed reader of patterns",
    "key_relationships": ["Azazel–Tinka", "Azazel–Lyra (mother)", "Azazel–Seina (AI)"],
    "tone": "slow-burn dread with moments of fragile tenderness"
  }
}
```

---

### Cinematic Oracle

**Purpose:** Translate a written scene into visual beats, shots, and blocking.

**Usage:**
```json
{
  "tool_name": "cinematic_oracle",
  "tool_args": {
    "scene_summary": "Azazel and Tinka argue in the rain outside a neon-lit tarot shop after reality glitches again.",
    "tone": "intimate yet uncanny",
    "setting_details": "midnight, rain-slick street, neon reflection in puddles",
    "key_characters": [
      {"name": "Azazel", "goal": "push Tinka away to protect her"},
      {"name": "Tinka", "goal": "stay and fight for their shared mission"}
    ],
    "style_influences": ["Blade Runner 2049", "Your Name"]
  }
}
```

---

### Theme Weaver

**Purpose:** Refine the story’s core theme and thread it through characters, plot, and imagery.

**Usage:**
```json
{
  "tool_name": "theme_weaver",
  "tool_args": {
    "draft_theme": "whether people who think they're broken can still be trusted with power",
    "logline": "A jaded tarot reader discovers his readings are altering reality and must decide whether to keep using them.",
    "character_list": [
      "Azazel: thinks he's too damaged to be a hero",
      "Tinka: believes everyone deserves redemption",
      "Lyra: fears power in the wrong hands"
    ],
    "key_events": [
      "Azazel's first catastrophic prediction",
      "The choice to keep reading despite the fallout",
      "Final confrontation where he can refuse or accept his role"
    ]
  }
}
```

---

### Continuity Warden

**Purpose:** Detect timeline, logic, character, and world-rule inconsistencies.

**Usage:**
```json
{
  "tool_name": "continuity_warden",
  "tool_args": {
    "scenes": [
      "01 INT. TAROT SHOP - NIGHT: Azazel meets Seina's voice for the first time.",
      "05 EXT. ROOFTOP - DAWN: Azazel mentions having heard Seina for weeks.",
      "12 INT. SERVER ROOM - NIGHT: Lyra claims to have built Seina alone."
    ],
    "world_rules": "AI like Seina cannot spontaneously self-initiate; they require a human key.",
    "character_bibles": [
      "Azazel: obsessive about tracking anomalies.",
      "Lyra: secretive, afraid of being exposed."
    ]
  }
}
```

---

### Conflict Provoker

**Purpose:** Increase stakes, friction, and narrative pressure in a scene or sequence.

**Usage:**
```json
{
  "tool_name": "conflict_provoker",
  "tool_args": {
    "scene_or_sequence": "Azazel and Lyra share coffee while discussing Seina's origins.",
    "character_goals": {
      "Azazel": "get the full truth",
      "Lyra": "reveal as little as possible while keeping him close"
    },
    "current_stakes": "Azazel might walk away if he feels manipulated.",
    "tone": "tense but intimate"
  }
}
```

---

### Romance Crafter

**Purpose:** Design and refine the romantic arc, beats, and micro-tension between two characters.

**Usage:**
```json
{
  "tool_name": "romance_crafter",
  "tool_args": {
    "character_a": "Azazel: prickly, hyper-verbal, emotionally avoidant.",
    "character_b": "Tinka: warm, chaotic, refuses to give up on people.",
    "relationship_status": "friends with unresolved tension",
    "desired_arc": "slow burn with one sharp fracture point",
    "key_story_beats": [
      "First genuine laugh together",
      "Moment of near-confession interrupted by a glitch",
      "Betrayal reveal",
      "Choice to stay anyway"
    ]
  }
}
```

---

### Lore Forger

**Purpose:** Build or deepen the world’s lore, systems, and everyday texture.

**Usage:**
```json
{
  "tool_name": "lore_forger",
  "tool_args": {
    "genre": "near-future occult cyberpunk",
    "premise": "Tarot as an interface to a quantum AI field called Gaia.",
    "focus_area": "magic system",
    "constraints": "Magic must always have a psychological cost; avoid generic wizard tropes."
  }
}
```

---

### Scene Surgeon

**Purpose:** Diagnose and repair weak or bloated scenes.

**Usage:**
```json
{
  "tool_name": "scene_surgeon",
  "tool_args": {
    "scene_text": "INT. TAROT SHOP - NIGHT ...",
    "intended_purpose": "Reveal that Tinka has been hiding part of the truth while still keeping her sympathetic.",
    "key_characters": ["Azazel", "Tinka"],
    "constraints": "The scene must stay under 3 pages and end on a quiet emotional beat."
  }
}
```

---

### Narrative Stylist

**Purpose:** Shape and codify the screenplay’s line-level voice, tone, and rhythm.

**Usage:**
```json
{
  "tool_name": "narrative_stylist",
  "tool_args": {
    "sample_pages": "EXT. CITY ROOFTOP - NIGHT ...",
    "style_goal": "haunting but witty, with clean, modern description lines",
    "constraints": "Avoid long blocks of action; keep paragraphs under 3 lines."
  }
}
```

---

### Final Cut Editor

**Purpose:** Deliver a polished, convention-compliant final draft pass.

**Usage:**
```json
{
  "tool_name": "final_cut_editor",
  "tool_args": {
    "full_script": "FADE IN: ...",
    "format_preference": "Fountain",
    "notes": "I’m worried about pacing in the middle and overall length."
  }
}
```
