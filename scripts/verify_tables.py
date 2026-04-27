import sqlite3
conn = sqlite3.connect('aria_test.db', timeout=30.0)
cursor = conn.cursor()
cursor.execute('PRAGMA journal_mode=WAL;')
cursor.execute('PRAGMA synchronous=NORMAL;')
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())
conn.close()
