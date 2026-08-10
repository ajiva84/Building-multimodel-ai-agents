"""Chapter 10 — a minimal MCP server wrapping the trade journal (read-only)."""
# pip install "mcp[cli]"
import json, sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("trade-journal")
db = sqlite3.connect("journal.db", check_same_thread=False)

@mcp.tool()
def get_setups(symbol: str, min_score: float = 7.0) -> str:
    """Return recent setups for a symbol at or above min_score,
    as JSON. Data comes from the journal database (read-only)."""
    rows = db.execute(
        "SELECT ts, symbol, score, outcome FROM setups "
        "WHERE symbol=? AND score>=? ORDER BY ts DESC LIMIT 20",
        (symbol, min_score)).fetchall()
    return json.dumps([dict(zip(("ts", "symbol", "score", "outcome"), r))
                       for r in rows])

if __name__ == "__main__":
    mcp.run()          # speaks the protocol over stdio
