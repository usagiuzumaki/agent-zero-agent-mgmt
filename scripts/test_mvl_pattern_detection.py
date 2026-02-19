import asyncio
import os
import sqlite3
import json
from python.helpers.mvl_manager import MVLManager

class MockAgent:
    async def call_utility_model(self, system, message):
        # Return a sample JSON response
        return json.dumps({
            "mask": "The Victim",
            "claims": [{"type": "identity_claim", "text": "I am helpless", "confidence": 0.9}],
            "signals": {"emotional_delta": -0.5, "defensiveness": 0.8, "stakes": 0.7},
            "pattern_candidates": [
                {
                    "type": "loop",
                    "summary": "User keeps repeating the same issue without trying solutions.",
                    "lore_weight": 0.8
                }
            ],
            "recommend_mt_gate": "confront"
        })

async def run_test():
    print("Starting MVL Pattern Detection Test...")

    db_path = "test_loom_pattern.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    mock_agent = MockAgent()
    manager = MVLManager(db_path=db_path, agent=mock_agent)

    user_id = "test_user_123"
    text = "I just can't do it. It keeps failing."

    print(f"Processing message: '{text}'")
    gate = await manager.process_message(user_id, text)
    print(f"Gate decision: {gate}")

    # Verify DB
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check interaction_event
    cursor.execute("SELECT pattern_ids, mt_gate FROM interaction_event WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    print(f"Interaction Event: pattern_ids={row[0]}, mt_gate={row[1]}")

    if row is None:
        print("Error: No interaction event found.")
        exit(1)

    pattern_ids = json.loads(row[0])
    if len(pattern_ids) == 0:
        print("Error: No pattern_ids found.")
        exit(1)

    # Check pattern_echo
    cursor.execute("SELECT * FROM pattern_echo WHERE id = ?", (pattern_ids[0],))
    pattern_row = cursor.fetchone()
    print(f"Pattern Echo: {pattern_row}")

    if pattern_row is None:
        print("Error: No pattern echo found.")
        exit(1)

    if pattern_row[2] != "loop":
        print(f"Error: Expected pattern type 'loop', got '{pattern_row[2]}'")
        exit(1)

    conn.close()

    # Clean up
    if os.path.exists(db_path):
        os.remove(db_path)

    print("Test PASSED!")

if __name__ == "__main__":
    asyncio.run(run_test())
