"""Chapter 13 — the daily cost report. Run from cron; message yourself."""
import json, collections

def report(path="runs.jsonl") -> str:
    spend = collections.Counter()
    for line in open(path):
        r = json.loads(line)
        spend[r.get("workflow", "unknown")] += r.get("cost", 0)
    return "\n".join(f"{w}: ${c:.2f}" for w, c in spend.most_common())

if __name__ == "__main__":
    print("💰 Yesterday by workflow:\n" + report())
    # STUB: send_telegram(...)
