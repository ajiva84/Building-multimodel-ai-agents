"""Chapter 8 — the critic: numbered rules, pass/fail, never edits."""

CRITIC_PROMPT = """You review trade alerts before they are sent.
Check ONLY these rules and reply as JSON
{"verdict": "pass"|"fail", "reasons": [...]}:
1. zone_score >= 7.0 is stated and justified by the data shown
2. An active session window is named
3. No numbers appear that are absent from the tool results
Be strict. A wrong alert costs real money; a delayed one costs little."""

def review(client, draft: str, model="claude-haiku-4-5-20251001") -> dict:
    import json
    r = client.messages.create(
        model=model, max_tokens=300, system=CRITIC_PROMPT,
        messages=[{"role": "user", "content": draft}])
    return json.loads(r.content[0].text)
# Loop author -> critic -> author at most TWICE, then escalate to a human.
