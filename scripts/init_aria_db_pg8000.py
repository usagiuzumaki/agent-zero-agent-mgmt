import os
import sys
import pg8000.native
from urllib.parse import urlparse

def main():
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("DATABASE_URL not found")
        return

    url = urlparse(db_url)
    host = url.hostname
    port = url.port or 5432
    database = url.path[1:]
    user = url.username
    password = url.password

    conn = pg8000.native.Connection(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password,
        ssl_context=True
    )

    # Create tables manually using raw SQL
    queries = [
        "CREATE TABLE IF NOT EXISTS users (id VARCHAR(255) PRIMARY KEY, email VARCHAR(255) UNIQUE NOT NULL)",
        "CREATE TABLE IF NOT EXISTS projects (id SERIAL PRIMARY KEY, user_id VARCHAR(255) REFERENCES users(id), name VARCHAR(255) NOT NULL, description TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS chapters (id SERIAL PRIMARY KEY, project_id INTEGER REFERENCES projects(id), title VARCHAR(255) NOT NULL, summary TEXT, poetic_epilogue TEXT, chapter_order INTEGER DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS pages (id SERIAL PRIMARY KEY, chapter_id INTEGER REFERENCES chapters(id), title VARCHAR(255), page_order INTEGER DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS blocks (id SERIAL PRIMARY KEY, page_id INTEGER REFERENCES pages(id), block_type VARCHAR(50) NOT NULL, content TEXT, block_order INTEGER DEFAULT 0, version INTEGER DEFAULT 1, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS aria_annotations (id SERIAL PRIMARY KEY, block_id INTEGER REFERENCES blocks(id), content TEXT NOT NULL, annotation_type VARCHAR(50), anchor_data TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS images (id SERIAL PRIMARY KEY, user_id VARCHAR(255) REFERENCES users(id), chapter_id INTEGER REFERENCES chapters(id), url VARCHAR(512) NOT NULL, filename VARCHAR(255), tone_tags VARCHAR(255), theme_labels VARCHAR(255), detected_meaning TEXT, reflective_caption TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS moodboard_items (id SERIAL PRIMARY KEY, user_id VARCHAR(255) REFERENCES users(id), project_id INTEGER REFERENCES projects(id), item_type VARCHAR(50) NOT NULL, content TEXT, x FLOAT DEFAULT 0, y FLOAT DEFAULT 0, z_index INTEGER DEFAULT 0, scale FLOAT DEFAULT 1, rotation FLOAT DEFAULT 0, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)",
        "CREATE TABLE IF NOT EXISTS growth_events (id SERIAL PRIMARY KEY, project_id INTEGER REFERENCES projects(id), event_type VARCHAR(50), description TEXT, milestone_marker VARCHAR(255), event_metadata TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    ]

    for q in queries:
        print(f"Running: {q[:50]}...")
        conn.run(q)

    print("Database initialization complete.")
    conn.close()

if __name__ == "__main__":
    main()
