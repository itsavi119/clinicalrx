import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "clinicalrx.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS sections")
cursor.execute("DROP TABLE IF EXISTS topics")
cursor.execute("DROP TABLE IF EXISTS subjects")

cursor.execute("""
CREATE TABLE subjects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    FOREIGN KEY (subject_id) REFERENCES subjects (id)
)
""")

cursor.execute("""
CREATE TABLE sections (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    content TEXT
)
""")

conn.commit()
conn.close()

print("Database reset successfully")