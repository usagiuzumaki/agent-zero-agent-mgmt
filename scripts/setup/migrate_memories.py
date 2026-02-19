import json
import os
import sqlite3
import uuid
from datetime import datetime

def migrate():
    json_path = 'aria_memories.json'
    db_path = 'loom.db'

    if not os.path.exists(json_path):
        print(f"No {json_path} found. Skipping migration.")
        return

    print(f"Migrating {json_path} to {db_path}...")

    with open(json_path, 'r') as f:
        memories = json.load(f)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Assume a default user_id since aria_memories.json wasn't multi-user
    user_id = "default_user"

    # Migrate memories (user_facts, special_moments, inside_jokes, etc.)
    categories = ['user_facts', 'special_moments', 'inside_jokes', 'preferences', 'milestones']
    for category in categories:
        items = memories.get(category, [])
        if isinstance(items, list):
            for item in items:
                content = item.get('content') if isinstance(item, dict) else str(item)
                ts = item.get('timestamp', datetime.now().isoformat()) if isinstance(item, dict) else datetime.now().isoformat()
                context = item.get('context') if isinstance(item, dict) else None

                cursor.execute('''
                    INSERT INTO personality_memory (id, user_id, category, content, context, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (str(uuid.uuid4()), user_id, category, content, context, ts))
        elif isinstance(items, dict):
            for key, item in items.items():
                content = item.get('content') if isinstance(item, dict) else str(item)
                ts = item.get('timestamp', datetime.now().isoformat()) if isinstance(item, dict) else datetime.now().isoformat()

                cursor.execute('''
                    INSERT INTO personality_memory (id, user_id, category, content, context, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (str(uuid.uuid4()), user_id, category, key + ": " + content, None, ts))

    # Migrate quiz answers
    quiz_answers = memories.get('quiz_answers', {})
    cursor.execute('''
        INSERT INTO personality_quiz (user_id, quiz_answers)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET quiz_answers = excluded.quiz_answers
    ''', (user_id, json.dumps(quiz_answers)))

    conn.commit()
    conn.close()
    print("Migration complete.")

if __name__ == "__main__":
    migrate()
