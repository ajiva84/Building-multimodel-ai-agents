"""Chapter 10 — a minimal MCP server wrapping price history (read-only)."""
# pip install "mcp[cli]"
import json, sqlite3
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("price-history")
db = sqlite3.connect("prices.db", check_same_thread=False)

@mcp.tool()
def get_price_history(route: str, days: int = 90) -> str:
    """Return recorded fares for a route over the last N days, as JSON.
    Data comes from the local price-history database (read-only)."""
    rows = db.execute(
        "SELECT ts, route, cabin, fare FROM prices "
        "WHERE route=? AND ts >= date('now', ?) ORDER BY ts DESC LIMIT 50",
        (route, f"-{days} days")).fetchall()
    return json.dumps([dict(zip(("ts", "route", "cabin", "fare"), r))
                       for r in rows])

if __name__ == "__main__":
    mcp.run()          # speaks the protocol over stdio
