import sqlite3
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).resolve().parent / "memory_log.db"

def init_db():
    """Initializes the SQLite database if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            input TEXT,
            output TEXT,
            tag TEXT
        )
    ''')
    conn.commit()
    return conn

def log_memory(input_text: str, output_text: str, tag: str = "general"):
    """Logs a single memory entry with optional tag."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    timestamp = str(datetime.now())
    c.execute('''
        INSERT INTO memory (timestamp, input, output, tag)
        VALUES (?, ?, ?, ?)
    ''', (timestamp, input_text, output_text, tag))
    conn.commit()
    conn.close()

def get_memories(tag: str = "general", limit: int = 10):
    """Retrieves the last N memory entries with a given tag."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT timestamp, input, output FROM memory
        WHERE tag = ?
        ORDER BY id DESC
        LIMIT ?
    ''', (tag, limit))
    results = c.fetchall()
    conn.close()
    return results
