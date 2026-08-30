# Building Multi-Model AI Agents — Companion Code

Working code for every chapter of *Building Multi-Model AI Agents* (First Edition, 2026).

## Structure

| Folder | Chapter | What's inside |
|---|---|---|
| `ch01_first_agent/` | 1 | The complete ~50-line agent |
| `ch02_adapter/` | 2 | Provider adapter + structured output repair loop |
| `ch04_tools/` | 4 | Tool registry with schema generation |
| `ch05_loop/` | 5 | Budgeted loop, flail detection, retries, run logs |
| `ch06_memory/` | 6 | Compaction, state objects, SQLite long-term memory |
| `ch07_knowledge/` | 7 | Minimal RAG stack + hybrid search |
| `ch08_orchestration/` | 8 | Router, pipeline, supervisor, critic |
| `ch09_routing/` | 9 | Model tiers + escalation ladder |
| `ch10_mcp/` | 10 | Minimal MCP server (FastMCP) |
| `ch11_evals/` | 11 | Golden-set runner, graders, trajectory checks |
| `ch12_guardrails/` | 12 | Action gates, approval queue, kill switch |
| `ch13_cost/` | 13 | Daily cost report |
| `ch14_deploy/` | 14 | Webhook receiver, worker, heartbeat, systemd unit |
| `projects/` | 15–17 | Skeletons for the three end-to-end projects |

## Setup

```bash
python3.11 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp secrets.env.example secrets.env   # then fill in your keys
```

Set `ANTHROPIC_API_KEY` (and optionally `GEMINI_API_KEY`) in your environment
or in `secrets.env` (which is git-ignored — never commit real keys).

## A note on stubs

Where the book shows `...` the code here keeps a clearly-marked stub with a
comment, so files run or fail loudly rather than pretending. Each folder's
code matches its chapter's listings; fill stubs with your own domain logic
(the book's examples use flight-price watching and retail operations).
