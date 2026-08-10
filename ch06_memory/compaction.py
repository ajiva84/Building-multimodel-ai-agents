"""Chapter 6 — compaction: summarize the middle, keep the edges."""
import json

def compact(client, messages: list, keep_recent: int = 6,
            trigger_at: int = 30) -> list:
    """Replace old turns with a summary once the transcript is long."""
    if len(messages) <= trigger_at:
        return messages

    old, recent = messages[:-keep_recent], messages[-keep_recent:]

    summary = client.messages.create(
        model="claude-haiku-4-5-20251001",       # cheap model, mechanical job
        max_tokens=800,
        messages=[{
            "role": "user",
            "content": (
                "Summarize this agent transcript for the agent's own future "
                "reference. PRESERVE EXACTLY: all numbers, IDs, symbols, "
                "file paths, decisions made and their reasons, and anything "
                "flagged as unresolved. DROP: pleasantries, dead ends already "
                "abandoned, verbose tool output.\n\n"
                + json.dumps(old, default=str)[:50_000]
            ),
        }],
    ).content[0].text

    return ([{"role": "user",
              "content": f"[SUMMARY OF EARLIER WORK]\n{summary}"}]
            + recent)
