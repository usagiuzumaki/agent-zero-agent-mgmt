## SQL

```sql
-- Table: interaction_event
CREATE TABLE interaction_event (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    role TEXT CHECK(role IN ('user', 'aria', 'system')),
    text TEXT,
    tokens INTEGER,
    channel TEXT CHECK(channel IN ('chat', 'voice', 'image', 'file')),
    intent_tag TEXT,
    utility_flag BOOLEAN,
    novelty REAL CHECK(novelty BETWEEN 0 AND 1),
    narrative_weight REAL CHECK(narrative_weight BETWEEN 0 AND 1),
    entropy_delta REAL CHECK(entropy_delta BETWEEN -1 AND 1),
    meaningfulness REAL CHECK(meaningfulness BETWEEN 0 AND 1),
    mt_gate TEXT CHECK(mt_gate IN ('silence', 'reply', 'refuse', 'delay', 'confront')),
    pattern_ids TEXT, -- JSON list of IDs
    embedding_id TEXT
);

-- Table: pattern_echo
CREATE TABLE pattern_echo (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    type TEXT CHECK(type IN ('contradiction', 'loop', 'confession', 'boundary', 'desire', 'fear', 'goal', 'identity_claim', 'trigger')),
    summary TEXT,
    evidence_event_ids TEXT, -- JSON list of event IDs
    first_seen_ts DATETIME,
    last_seen_ts DATETIME,
    strength REAL CHECK(strength BETWEEN 0 AND 1),
    recency REAL CHECK(recency BETWEEN 0 AND 1),
    lore_weight REAL CHECK(lore_weight BETWEEN 0 AND 1),
    status TEXT CHECK(status IN ('active', 'resolved', 'dormant', 'retired')),
    embedding_id TEXT
);

-- Table: archetype_state
CREATE TABLE archetype_state (
    id TEXT PRIMARY KEY,
    user_id TEXT NOT NULL,
    ts DATETIME DEFAULT CURRENT_TIMESTAMP,
    axes TEXT, -- JSON object: { "rebel": 0.12, ... }
    delta_axes TEXT, -- JSON object: change vs last checkpoint
    confidence REAL CHECK(confidence BETWEEN 0 AND 1),
    source_pattern_ids TEXT -- JSON list of pattern IDs
);

-- Table: loom_state
CREATE TABLE loom_state (
    user_id TEXT PRIMARY KEY,
    entropy REAL CHECK(entropy BETWEEN 0 AND 1),
    dormancy BOOLEAN,
    last_active_ts DATETIME,
    silence_streak INTEGER,
    dependency_risk REAL CHECK(dependency_risk BETWEEN 0 AND 1),
    mask_weights TEXT, -- JSON object: { "subtext": 0.4, ... }
    last_archetype_state_id TEXT,
    FOREIGN KEY(last_archetype_state_id) REFERENCES archetype_state(id)
);
```

## JSON_SCHEMA

```json
{
  "MaskOutput": {
    "type": "object",
    "properties": {
      "mask": { "type": "string" },
      "claims": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "type": { "type": "string" },
            "text": { "type": "string" },
            "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        }
      },
      "signals": {
        "type": "object",
        "properties": {
          "emotional_delta": { "type": "number" },
          "defensiveness": { "type": "number" },
          "stakes": { "type": "number" }
        }
      },
      "pattern_candidates": {
        "type": "array",
        "items": {
          "type": "object",
          "properties": {
            "type": { "type": "string" },
            "summary": { "type": "string" },
            "lore_weight": { "type": "number", "minimum": 0, "maximum": 1 }
          }
        }
      },
      "recommend_mt_gate": { "type": "string", "enum": ["silence", "reply", "refuse", "delay", "confront"] }
    },
    "required": ["mask", "claims", "signals", "pattern_candidates"]
  },
  "PatternEchoRecord": {
    "type": "object",
    "properties": {
      "id": { "type": "string" },
      "type": { "type": "string" },
      "summary": { "type": "string" },
      "evidence_event_ids": { "type": "array", "items": { "type": "string" } },
      "strength": { "type": "number", "minimum": 0, "maximum": 1 },
      "recency": { "type": "number", "minimum": 0, "maximum": 1 },
      "lore_weight": { "type": "number", "minimum": 0, "maximum": 1 },
      "status": { "type": "string", "enum": ["active", "resolved", "dormant", "retired"] }
    },
    "required": ["id", "type", "summary", "evidence_event_ids", "strength", "recency", "lore_weight", "status"]
  },
  "ANLDecision": {
    "type": "object",
    "properties": {
      "novelty": { "type": "number", "minimum": 0, "maximum": 1 },
      "narrative_weight": { "type": "number", "minimum": 0, "maximum": 1 },
      "interaction_entropy": { "type": "number", "minimum": 0, "maximum": 1 },
      "meaningfulness": { "type": "number", "minimum": 0, "maximum": 1 },
      "mt_gate": { "type": "string", "enum": ["silence", "reply", "refuse", "delay", "confront"] },
      "reasons": { "type": "array", "items": { "type": "string" } },
      "pattern_ids": { "type": "array", "items": { "type": "string" } }
    },
    "required": ["novelty", "narrative_weight", "interaction_entropy", "meaningfulness", "mt_gate", "reasons", "pattern_ids"]
  }
}
```

## PSEUDOCODE

```python
def compute_entropy(current_entropy, novelty, pattern_repeat_48h):
    # Heuristic for updating interaction entropy
    new_entropy = current_entropy
    if novelty < 0.3:
        new_entropy += 0.08
    if novelty > 0.6:
        new_entropy -= 0.06
    if pattern_repeat_48h:
        new_entropy += 0.10
    return max(0.0, min(1.0, new_entropy))

def decide_mt_gate(meaningfulness, narrative_weight, utility_flag, mask_conflict, self_sabotage):
    # Logic for Meaningfulness Threshold gate
    if meaningfulness < 0.25:
        return "silence"
    if utility_flag and narrative_weight < 0.5:
        return "refuse"
    if mask_conflict:
        return "delay"
    if meaningfulness > 0.75 and self_sabotage:
        return "confront"
    return "reply"
```
