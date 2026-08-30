"""Chapter 4 — example tools showing description craft and rich errors."""
import json
from registry import ToolRegistry

registry = ToolRegistry()
AIRPORTS = {"LHR", "JFK", "DXB", "SIN", "IAH"}

@registry.register
def get_fare(route: str, cabin: str) -> str:
    """Get the current lowest fare for a route. Call this before every
    comparison — never reuse a fare from earlier in the conversation.
    Route format: 'LHR-JFK'. Cabin: economy, premium, or business.
    Supported airports: LHR, JFK, DXB, SIN, IAH."""
    origin, _, dest = route.partition("-")
    unknown = [a for a in (origin, dest) if a not in AIRPORTS]
    if unknown:
        return json.dumps({
            "error": "unknown_airport",
            "message": f"{unknown} not recognized.",
            "supported_airports": sorted(AIRPORTS),   # the fix, handed over
        })
    # STUB: real fare lookup goes here
    return json.dumps({"route": route, "cabin": cabin,
                       "fare": 412, "currency": "USD"})

@registry.register
def send_telegram_alert(message: str) -> str:
    """Send a fare alert to the Telegram channel.
    Use ONLY when the fare is at or below the user's target price AND
    seats are still available. For prices above target, or to record a
    price history point, use log_price instead.
    Sends immediately and cannot be recalled."""
    # STUB: real Telegram sendMessage call goes here
    return json.dumps({"sent": True})
