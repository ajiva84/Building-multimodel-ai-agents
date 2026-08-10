"""Chapter 12 — the action gate: the model gets a vote, never a veto."""
import json
from pathlib import Path

LIMITS = {"send_telegram_alert": {"per_hour": 3},
          "update_sheet":        {"per_hour": 20}}
IRREVERSIBLE = {"send_telegram_alert", "post_social", "pay_invoice"}

def deny(code: str, detail: str) -> str:
    return json.dumps({"denied": code, "detail": detail})

def kill_switch_active() -> bool:
    return Path("/opt/agent/KILL").exists()

def gated_execute(registry, name: str, args: dict, ctx) -> str:
    """ctx needs: allowed_tools (set), plus your domain helpers below."""
    # 1. Policy: least privilege per agent
    if name not in ctx.allowed_tools:
        return deny("tool_not_permitted", name)
    # 2. Rate limits: code-counted, not model-remembered
    if ctx.over_limit(name, LIMITS):
        return deny("rate_limited", f"{name} hit {LIMITS.get(name)}")
    # 3. Domain rules: recompute, don't trust
    if name == "send_telegram_alert":
        score = ctx.recompute_zone_score(args)
        if score < 7.0:
            return deny("below_threshold", f"recomputed score {score}")
        if not ctx.session_window_active():
            return deny("outside_session", "no active session window")
    # 4. Irreversible -> human
    if name in IRREVERSIBLE:
        return ctx.queue_for_approval(name, args)
    return registry.execute(name, args)
