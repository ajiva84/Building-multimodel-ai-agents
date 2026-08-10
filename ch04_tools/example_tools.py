"""Chapter 4 — example tools showing description craft and rich errors."""
import json
from registry import ToolRegistry

registry = ToolRegistry()
SUPPORTED = {"EURUSD", "GBPUSD", "XAUUSD", "USDJPY"}

@registry.register
def get_ohlc(symbol: str, timeframe: str) -> str:
    """Get OHLC candles for a forex pair. Use before any zone analysis.
    Supported symbols: EURUSD, GBPUSD, XAUUSD, USDJPY.
    Supported timeframes: M15, H1, H4, D1."""
    if symbol not in SUPPORTED:
        return json.dumps({
            "error": "unsupported_symbol",
            "message": f"'{symbol}' is not supported.",
            "supported_symbols": sorted(SUPPORTED),   # the fix, handed over
        })
    # STUB: real data fetch goes here
    return json.dumps({"symbol": symbol, "timeframe": timeframe,
                       "candles": [{"o": 1.084, "h": 1.087,
                                    "l": 1.083, "c": 1.086}]})

@registry.register
def send_telegram_alert(message: str) -> str:
    """Send a trade alert to the Telegram channel.
    Use ONLY for setups with zone_score >= 7.0 during an active session
    window. Do NOT use for journaling, questions, or sub-threshold setups —
    use log_to_journal for those. Sends immediately and cannot be recalled."""
    # STUB: real Telegram sendMessage call goes here
    return json.dumps({"sent": True})
