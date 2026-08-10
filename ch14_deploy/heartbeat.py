"""Chapter 14 — the morning heartbeat. Silence must be a symptom."""
import sqlite3

def counts(db):
    ran    = db.execute("SELECT COUNT(*) FROM jobs").fetchone()[0]
    failed = db.execute("SELECT COUNT(*) FROM jobs "
                        "WHERE status='failed'").fetchone()[0]
    return ran, failed

if __name__ == "__main__":
    db = sqlite3.connect("jobs.db")
    ran, failed = counts(db)
    msg = f"☀️ Agent morning report\nJobs: {ran} ran, {failed} failed"
    print(msg)
    # STUB: send_telegram(msg)
    # Plus a dead-man's switch: an external check that alarms if THIS
    # heartbeat itself goes silent.
