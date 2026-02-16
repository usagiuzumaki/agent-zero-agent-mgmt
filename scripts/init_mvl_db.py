import sqlite3
import os

def init_db():
    db_path = 'loom.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # interaction_event
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS interaction_event (
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
        pattern_ids TEXT,
        embedding_id TEXT
    )
    ''')

    # pattern_echo
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pattern_echo (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        type TEXT CHECK(type IN ('contradiction', 'loop', 'confession', 'boundary', 'desire', 'fear', 'goal', 'identity_claim', 'trigger')),
        summary TEXT,
        evidence_event_ids TEXT,
        first_seen_ts DATETIME,
        last_seen_ts DATETIME,
        strength REAL CHECK(strength BETWEEN 0 AND 1),
        recency REAL CHECK(recency BETWEEN 0 AND 1),
        lore_weight REAL CHECK(lore_weight BETWEEN 0 AND 1),
        status TEXT CHECK(status IN ('active', 'resolved', 'dormant', 'retired')),
        embedding_id TEXT
    )
    ''')

    # archetype_state
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS archetype_state (
        id TEXT PRIMARY KEY,
        user_id TEXT NOT NULL,
        ts DATETIME DEFAULT CURRENT_TIMESTAMP,
        axes TEXT,
        delta_axes TEXT,
        confidence REAL CHECK(confidence BETWEEN 0 AND 1),
        source_pattern_ids TEXT
    )
    ''')

    # loom_state
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS loom_state (
        user_id TEXT PRIMARY KEY,
        entropy REAL CHECK(entropy BETWEEN 0 AND 1),
        dormancy BOOLEAN,
        last_active_ts DATETIME,
        silence_streak INTEGER,
        dependency_risk REAL CHECK(dependency_risk BETWEEN 0 AND 1),
        mask_weights TEXT,
        last_archetype_state_id TEXT,
        FOREIGN KEY(last_archetype_state_id) REFERENCES archetype_state(id)
    )
    ''')

    conn.commit()
    conn.close()
    print(f"Database initialized at {os.path.abspath(db_path)}")

if __name__ == "__main__":
    init_db()
