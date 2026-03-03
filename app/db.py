import sqlite3
from pathlib import Path

DB_PATH = Path("/data/toolbox.sqlite")

SCHEMA = """
CREATE TABLE IF NOT EXISTS events (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  ts DATETIME DEFAULT CURRENT_TIMESTAMP,
  kind TEXT NOT NULL,
  idempotency_key TEXT,
  payload_json TEXT NOT NULL,
  status TEXT NOT NULL,
  result_json TEXT
);
CREATE UNIQUE INDEX IF NOT EXISTS idx_events_idem ON events(idempotency_key) WHERE idempotency_key IS NOT NULL;
"""

def get_conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    conn.executescript(SCHEMA)
    return conn