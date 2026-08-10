"""Chapter 14 — the worker: a separate process that does everything."""
import time, sqlite3

db = sqlite3.connect("jobs.db")

def claim_next_job():
    row = db.execute("SELECT id, kind, payload FROM jobs "
                     "WHERE status='queued' ORDER BY id LIMIT 1").fetchone()
    if row:
        db.execute("UPDATE jobs SET status='running' WHERE id=?", (row[0],))
        db.commit()
    return row

def run_agent_for(job):
    """STUB: route job.kind to the right budgeted, gated agent (Ch. 5, 12)."""
    raise NotImplementedError

if __name__ == "__main__":
    while True:
        job = claim_next_job()
        if not job:
            time.sleep(2); continue
        try:
            result = run_agent_for(job)
            db.execute("UPDATE jobs SET status='done', result=? WHERE id=?",
                       (str(result), job[0]))
        except Exception as e:
            db.execute("UPDATE jobs SET status='failed', result=? WHERE id=?",
                       (str(e), job[0]))    # parked, never lost
        db.commit()
