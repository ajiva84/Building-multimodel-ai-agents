"""Chapter 6 — long-term memory: a SQLite table, not a vector database."""
import sqlite3, datetime, json

def init_memory(path="agent_memory.db"):
    db = sqlite3.connect(path)
    db.execute("""CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY,
        ts TEXT, kind TEXT, key TEXT, value TEXT)""")
    return db

def remember(db, kind: str, key: str, value: dict):
    db.execute("INSERT INTO memories (ts, kind, key, value) VALUES (?,?,?,?)",
               (datetime.datetime.now(datetime.timezone.utc).isoformat(),
                kind, key, json.dumps(value)))
    db.commit()

def recall(db, kind: str, key: str | None = None, limit: int = 10):
    q = "SELECT ts, key, value FROM memories WHERE kind=?"
    args = [kind]
    if key:
        q += " AND key=?"; args.append(key)
    q += " ORDER BY ts DESC LIMIT ?"; args.append(limit)
    return db.execute(q, args).fetchall()
