import sqlite3
import uuid
import asyncio
from typing import Optional, List, Any
import logging
from datetime import datetime

from python.helpers import loom_logic
from python.helpers import files
from python.helpers.print_style import PrintStyle
from python.helpers.dirty_json import DirtyJson
from difflib import SequenceMatcher

class MVLManager:
    def __init__(self, db_path="loom.db", agent=None):
        self.db_path = files.get_abs_path(db_path)
        self.agent = agent
        self._init_db()

    def get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        conn = self.get_connection()
        cursor = conn.cursor()

        # Check if tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='loom_state'")
        if not cursor.fetchone():
             # Execute initialization SQL
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
            print(f"MVL Database initialized at {self.db_path}")
        else:
            # Check for pattern_echo table
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pattern_echo'")
            if not cursor.fetchone():
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
                conn.commit()
                print(f"Added pattern_echo table to {self.db_path}")

            # Check for pattern_ids column in interaction_event
            cursor.execute("PRAGMA table_info(interaction_event)")
            columns = [info[1] for info in cursor.fetchall()]
            if 'pattern_ids' not in columns:
                try:
                    cursor.execute("ALTER TABLE interaction_event ADD COLUMN pattern_ids TEXT")
                    conn.commit()
                    print(f"Added pattern_ids column to interaction_event in {self.db_path}")
                except Exception as e:
                    PrintStyle().print(f"Migration error (pattern_ids): {e}")

        conn.close()

    def get_state(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT entropy, silence_streak FROM loom_state WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            return {"entropy": row[0], "silence_streak": row[1]}
        return {"entropy": 0.5, "silence_streak": 0} # Default

    def update_state(self, user_id, entropy, silence_streak):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO loom_state (user_id, entropy, silence_streak, last_active_ts)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ON CONFLICT(user_id) DO UPDATE SET
            entropy = excluded.entropy,
            silence_streak = excluded.silence_streak,
            last_active_ts = CURRENT_TIMESTAMP
        ''', (user_id, entropy, silence_streak))
        conn.commit()
        conn.close()

    async def calculate_novelty_async(self, text: str, user_id: str) -> float:
        # 1. Try embedding model if available and we had a vector store (not implemented yet)
        # 2. Fallback to sequence matching with recent history
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT text FROM interaction_event WHERE user_id = ? ORDER BY ts DESC LIMIT 5", (user_id,))
            recent_texts = [r[0] for r in cursor.fetchall()]
            conn.close()

            if not recent_texts:
                return 1.0 # Max novelty if no history

            max_sim = 0.0
            for prev_text in recent_texts:
                if prev_text:
                    sim = SequenceMatcher(None, text, prev_text).ratio()
                    if sim > max_sim:
                        max_sim = sim

            # Novelty is inverse of similarity
            return 1.0 - max_sim

        except Exception as e:
            PrintStyle().print(f"Novelty calculation error: {e}")
            return 0.5

    def calculate_narrative_weight_heuristic(self, text: str) -> float:
        text_lower = text.lower()
        has_desire_fear = any(w in text_lower for w in ["want", "need", "scared", "afraid", "fear", "desire", "wish", "hope"])
        references_past = any(w in text_lower for w in ["remember", "before", "ago", "last time", "yesterday", "used to"])
        is_decision = any(w in text_lower for w in ["should i", "what if", "choice", "decide", "option"])
        is_identity = any(w in text_lower for w in ["i am", "i'm a", "my personality", "who i am"])

        return loom_logic.calculate_narrative_weight(
            has_desire_fear_confession=has_desire_fear,
            references_past=references_past,
            is_decision_point=is_decision,
            is_identity_statement=is_identity
        )

    async def detect_pattern(self, user_id: str, text: str) -> Optional[str]:
        if not self.agent:
            return None

        # 1. Fetch recent history (last 10 events)
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role, text FROM interaction_event WHERE user_id = ? ORDER BY ts DESC LIMIT 10", (user_id,))
        history_rows = cursor.fetchall()
        conn.close()

        # Reverse to chronological order
        history_rows.reverse()
        history_text = "\n".join([f"{role}: {msg}" for role, msg in history_rows])

        # 2. Call LLM
        system_prompt = """
        Analyze the conversation history for recurring psychological patterns.
        Look for:
        - Contradiction: Saying one thing, doing another.
        - Loop: Repeating the same issue without resolution.
        - Confession: Admitting a hidden truth.
        - Boundary: Testing limits.
        - Desire: Expressing a want.
        - Fear: Expressing anxiety.
        - Goal: Stating an objective.
        - Identity Claim: "I am X".
        - Trigger: Specific topic causing reaction.

        Return JSON:
        {
            "pattern_found": boolean,
            "type": "loop" | "contradiction" | "confession" | "boundary" | "desire" | "fear" | "goal" | "identity_claim" | "trigger",
            "summary": "User keeps asking about X...",
            "strength": 0.0 to 1.0,
            "evidence_quotes": ["quote 1", "quote 2"]
        }
        """

        try:
            response_str = await self.agent.call_utility_model(
                system=system_prompt,
                message=f"History:\n{history_text}\n\nCurrent Message:\n{text}"
            )

            data = DirtyJson.parse_string(response_str)
            if not isinstance(data, dict):
                return None

            if data.get("pattern_found") and data.get("strength", 0) > 0.6:
                pattern_id = str(uuid.uuid4())
                pattern_type = data.get("type", "unknown")
                summary = data.get("summary", "")
                strength = data.get("strength", 0)

                # Insert into pattern_echo
                conn = self.get_connection()
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO pattern_echo (
                        id, user_id, type, summary, first_seen_ts, last_seen_ts, strength, recency, lore_weight, status
                    ) VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, 1.0, 0.5, 'active')
                ''', (pattern_id, user_id, pattern_type, summary, strength))
                conn.commit()
                conn.close()

                return pattern_id

        except Exception as e:
            PrintStyle().print(f"Pattern detection error: {e}")

        return None

    async def process_message(self, user_id: str, text: str, role="user"):
        state = self.get_state(user_id)
        current_entropy = state["entropy"]
        silence_streak = state["silence_streak"]

        novelty = await self.calculate_novelty_async(text, user_id)
        narrative_weight = self.calculate_narrative_weight_heuristic(text)

        # Detect pattern
        pattern_id = await self.detect_pattern(user_id, text)
        pattern_repeat = False
        if pattern_id:
            pattern_repeat = True # Simplified for now: if a pattern is strong enough to be detected, it counts as repeating/echoing behavior

        new_entropy = loom_logic.compute_entropy(current_entropy, novelty, pattern_repeat)
        meaningfulness = loom_logic.calculate_meaningfulness(narrative_weight, novelty, new_entropy)

        # Utility flag: check if user asks for task
        utility_flag = any(w in text.lower() for w in ["code", "write", "fix", "search", "create", "generate"])

        mt_gate = loom_logic.decide_mt_gate(
            meaningfulness=meaningfulness,
            narrative_weight=narrative_weight,
            utility_flag=utility_flag,
            mask_conflict=False, # Placeholder
            self_sabotage=False # Placeholder
        )

        # Record event
        event_id = str(uuid.uuid4())
        pattern_ids_str = f'["{pattern_id}"]' if pattern_id else None

        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO interaction_event (
                id, user_id, role, text, novelty, narrative_weight,
                entropy_delta, meaningfulness, mt_gate, utility_flag, pattern_ids
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            event_id, user_id, role, text, novelty, narrative_weight,
            new_entropy - current_entropy, meaningfulness, mt_gate, utility_flag, pattern_ids_str
        ))
        conn.commit()
        conn.close()

        # Update state
        new_silence_streak = silence_streak + 1 if mt_gate == "silence" else 0
        self.update_state(user_id, new_entropy, new_silence_streak)

        return mt_gate
