"""Chapter 12 — async approval queue: agent finishes; you tap yes/no later.
The executor runs EXACTLY the approved payload — byte-for-byte."""
import sqlite3, json, datetime

def init(db_path="jobs.db"):
    db = sqlite3.connect(db_path)
    db.execute("""CREATE TABLE IF NOT EXISTS approvals (
        id INTEGER PRIMARY KEY, ts TEXT, tool TEXT, payload TEXT,
        status TEXT DEFAULT 'pending')""")
    return db

def queue_for_approval(db, tool: str, args: dict) -> str:
    db.execute("INSERT INTO approvals (ts, tool, payload) VALUES (?,?,?)",
               (datetime.datetime.now(datetime.timezone.utc).isoformat(),
                tool, json.dumps(args, sort_keys=True)))
    db.commit()
    # STUB: send Telegram message with inline [Yes]/[No] buttons + preview
    return json.dumps({"queued_for_approval": tool})

def execute_approved(db, registry, approval_id: int) -> str:
    row = db.execute("SELECT tool, payload FROM approvals "
                     "WHERE id=? AND status='pending'",
                     (approval_id,)).fetchone()
    if not row:
        return "not found or already handled"
    tool, payload = row
    result = registry.execute(tool, json.loads(payload))  # exact payload
    db.execute("UPDATE approvals SET status='executed' WHERE id=?",
               (approval_id,))
    db.commit()
    return result
