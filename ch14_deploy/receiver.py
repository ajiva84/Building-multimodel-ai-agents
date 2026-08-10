"""Chapter 14 — the webhook receiver: acks in milliseconds, on purpose."""
import json, sqlite3
from fastapi import FastAPI, Request, HTTPException

app = FastAPI()
db = sqlite3.connect("jobs.db", check_same_thread=False)
db.execute("""CREATE TABLE IF NOT EXISTS jobs (
    id INTEGER PRIMARY KEY, kind TEXT, payload TEXT,
    status TEXT DEFAULT 'queued', result TEXT)""")

def valid_signature(req) -> bool:
    # STUB: verify shared secret / HMAC from your webhook source
    return True

@app.post("/hook/tradingview")
async def hook(req: Request):
    payload = await req.json()
    if not valid_signature(req):
        raise HTTPException(403)
    db.execute("INSERT INTO jobs (kind, payload) VALUES (?,?)",
               ("tv_alert", json.dumps(payload)))
    db.commit()
    return {"ok": True}                   # acked in milliseconds
