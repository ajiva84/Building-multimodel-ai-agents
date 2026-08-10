"""Chapter 9 — model tiers in one config dict behind the adapter."""

MODELS = {
    "route":     "anthropic/claude-haiku-4-5-20251001",   # tier 3
    "extract":   "anthropic/claude-haiku-4-5-20251001",   # tier 3
    "act":       "anthropic/claude-sonnet-4-6",            # tier 2
    "plan":      "anthropic/claude-opus-4-8",              # tier 1
}
FALLBACK = {  # providers have bad days
    "anthropic/claude-sonnet-4-6": "google/gemini-flash",
}
