"""Chapter 6 — the state object: code-owned facts, rendered fresh each turn."""
import json
from dataclasses import dataclass, asdict, field

@dataclass
class TradeWatchState:
    symbol: str
    zone_low: float
    zone_high: float
    zone_score: float
    session_active: bool
    alert_sent: bool          # the field that prevents double-sends
    notes: list = field(default_factory=list)

def render_state(s) -> str:
    return ("CURRENT STATE (authoritative — trust this over the "
            "transcript):\n" + json.dumps(asdict(s), indent=2))
