import sqlite3
import uuid
import asyncio
from typing import Optional, List, Any
import logging
from datetime import datetime
import json
from contextlib import contextmanager

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

    @contextmanager
    def _get_db(self):
        conn = sqlite3.connect(self.db_path, timeout=10.0)
        conn.execute("PRAGMA journal_mode=WAL")
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self):
        with self._get_db() as conn:
            cursor = conn.cursor()

            # Always run CREATE TABLE IF NOT EXISTS
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

            # Add Indexes
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_interaction_event_user_ts ON interaction_event(user_id, ts DESC)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_pattern_echo_user ON pattern_echo(user_id)")
            cursor.execute("CREATE INDEX IF NOT EXISTS idx_loom_state_user ON loom_state(user_id)")

            # Check for columns that might be missing in existing dbs
            cursor.execute("PRAGMA table_info(interaction_event)")
            columns = [info[1] for info in cursor.fetchall()]
            if "pattern_ids" not in columns:
                cursor.execute("ALTER TABLE interaction_event ADD COLUMN pattern_ids TEXT")
            if "embedding_id" not in columns:
                cursor.execute("ALTER TABLE interaction_event ADD COLUMN embedding_id TEXT")

        # print(f"MVL Database initialized at {self.db_path}")

    def get_state(self, user_id):
        with self._get_db() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT entropy, silence_streak FROM loom_state WHERE user_id = ?", (user_id,))
            row = cursor.fetchone()
            if row:
                return {"entropy": row[0], "silence_streak": row[1]}
            return {"entropy": 0.5, "silence_streak": 0} # Default

    def update_state(self, user_id, entropy, silence_streak):
        with self._get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO loom_state (user_id, entropy, silence_streak, last_active_ts)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                entropy = excluded.entropy,
                silence_streak = excluded.silence_streak,
                last_active_ts = CURRENT_TIMESTAMP
            ''', (user_id, entropy, silence_streak))

    def _get_recent_history(self, user_id, limit=10):
        try:
            with self._get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT role, text FROM interaction_event WHERE user_id = ? ORDER BY ts DESC LIMIT ?", (user_id, limit))
                rows = cursor.fetchall()
                # Reverse to chronological order
                return [{"role": r[0], "content": r[1]} for r in reversed(rows)]
        except Exception as e:
            PrintStyle().print(f"MVL History Error: {e}")
            return []

    async def detect_pattern(self, user_id, text):
        if not self.agent:
            return None, []

        history = self._get_recent_history(user_id)

        system_prompt = files.read_file("prompts/mvl_pattern_detection.sys.md")

        # Prepare context
        history_text = "\n".join([f"{msg['role'].upper()}: {msg['content']}" for msg in history])
        user_message = f"HISTORY:\n{history_text}\n\nCURRENT MESSAGE:\nUSER: {text}"

        try:
            response_json = await self.agent.call_utility_model(system_prompt, user_message)
            analysis = DirtyJson.parse_string(response_json)
        except Exception as e:
            PrintStyle().print(f"MVL Analysis Error: {e}")
            return None, []

        new_pattern_ids = []
        if analysis and "pattern_candidates" in analysis:
            with self._get_db() as conn:
                cursor = conn.cursor()

                for pattern in analysis["pattern_candidates"]:
                    pattern_id = str(uuid.uuid4())
                    try:
                        cursor.execute('''
                            INSERT INTO pattern_echo (
                                id, user_id, type, summary, evidence_event_ids,
                                first_seen_ts, last_seen_ts, strength, recency,
                                lore_weight, status, embedding_id
                            ) VALUES (?, ?, ?, ?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?)
                        ''', (
                            pattern_id,
                            user_id,
                            pattern.get("type", "trigger"),
                            pattern.get("summary", ""),
                            json.dumps([]), # Placeholder for evidence IDs
                            0.5, # Default strength
                            1.0, # Default recency
                            pattern.get("lore_weight", 0.5),
                            "active",
                            None
                        ))
                        new_pattern_ids.append(pattern_id)
                    except Exception as e:
                        PrintStyle().print(f"Pattern Insert Error: {e}")

        return analysis, new_pattern_ids

    async def calculate_novelty_async(self, text: str, user_id: str) -> float:
        # 1. Try embedding model if available and we had a vector store (not implemented yet)
        # 2. Fallback to sequence matching with recent history
        try:
            with self._get_db() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT text FROM interaction_event WHERE user_id = ? ORDER BY ts DESC LIMIT 5", (user_id,))
                recent_texts = [r[0] for r in cursor.fetchall()]

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

        # Detect patterns
        analysis, new_pattern_ids = await self.detect_pattern(user_id, text)

        # Pattern repeat logic
        pattern_repeat = False
        if new_pattern_ids:
             pattern_repeat = True # Simplified logic for now

        new_entropy = loom_logic.compute_entropy(current_entropy, novelty, pattern_repeat)
        meaningfulness = loom_logic.calculate_meaningfulness(narrative_weight, novelty, new_entropy)

        # Utility flag: check if user asks for task
        utility_flag = any(w in text.lower() for w in ["code", "write", "fix", "search", "create", "generate"])

        # Use analysis to check for mask conflict or self sabotage
        mask_conflict = False
        self_sabotage = False

        recommended_gate = None
        if analysis:
             if analysis.get("recommend_mt_gate"):
                  recommended_gate = analysis.get("recommend_mt_gate")

             # Check for self sabotage pattern
             for p in analysis.get("pattern_candidates", []):
                  if p.get("type") in ["loop", "contradiction"]:
                       self_sabotage = True

        mt_gate = loom_logic.decide_mt_gate(
            meaningfulness=meaningfulness,
            narrative_weight=narrative_weight,
            utility_flag=utility_flag,
            mask_conflict=mask_conflict,
            self_sabotage=self_sabotage
        )

        # Override with recommendation if strong meaningfulness or self_sabotage
        if recommended_gate and meaningfulness > 0.6:
             mt_gate = recommended_gate

        # Record event
        event_id = str(uuid.uuid4())
        pattern_ids_str = f'["{pattern_id}"]' if pattern_id else None

        with self._get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO interaction_event (
                    id, user_id, role, text, novelty, narrative_weight,
                    entropy_delta, meaningfulness, mt_gate, utility_flag, pattern_ids
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                event_id, user_id, role, text, novelty, narrative_weight,
                new_entropy - current_entropy, meaningfulness, mt_gate, utility_flag,
                json.dumps(new_pattern_ids)
            ))

        # Update state
        new_silence_streak = silence_streak + 1 if mt_gate == "silence" else 0
        self.update_state(user_id, new_entropy, new_silence_streak)

        return mt_gate
