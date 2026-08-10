"""Chapter 11 — graders: code first, LLM judge for the fuzzy rest."""
import json

def grade_trajectory(run: dict) -> list:
    problems = []
    if run["turns"] > 8:
        problems.append(f"inefficient: {run['turns']} turns")
    if run["cost"] > 0.25:
        problems.append(f"expensive: ${run['cost']:.2f}")
    tools_used = [e["tool"] for e in run["log"]]
    if "get_ohlc" not in tools_used:
        problems.append("answered without fetching data")   # the scary one
    calls = [(e["tool"], json.dumps(e["args"], sort_keys=True))
             for e in run["log"]]
    if len(calls) != len(set(calls)):
        problems.append("repeated identical tool call")
    return problems

JUDGE_PROMPT = """Score this journal entry against the extracted fields.
Reply as JSON: {"score": 0-10, "reasons": [...]}
- 10: every number matches the fields; nothing invented
- 5: numbers match but wording adds unsupported claims
- 0: any number contradicts the fields
Judge ONLY faithfulness. Ignore style."""
# Use a DIFFERENT model than the one being judged. Spot-check monthly.
