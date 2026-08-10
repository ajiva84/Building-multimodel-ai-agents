"""Chapter 5 — the budgeted loop: the code that's actually in charge."""
import time, json, random, uuid, datetime
import anthropic
from dataclasses import dataclass, field

# Prices per million tokens — keep in config, they change.
PRICE = {"claude-sonnet-4-6": {"in": 3.00, "out": 15.00}}

@dataclass
class Budget:
    max_turns: int = 12
    max_cost_usd: float = 0.50
    max_seconds: float = 120.0

@dataclass
class RunState:
    turns: int = 0
    cost_usd: float = 0.0
    started: float = field(default_factory=time.monotonic)

    def exceeded(self, b: Budget) -> str | None:
        if self.turns >= b.max_turns:        return "turn_budget"
        if self.cost_usd >= b.max_cost_usd:  return "cost_budget"
        if time.monotonic() - self.started >= b.max_seconds:
            return "time_budget"
        return None

def is_flailing(log, window: int = 3) -> bool:
    """True if the last `window` tool calls are identical."""
    if len(log) < window:
        return False
    recent = [(e["tool"], json.dumps(e["args"], sort_keys=True))
              for e in log[-window:]]
    return len(set(recent)) == 1

def with_retries(fn, max_attempts=5, base=1.0):
    """Transport retries with exponential backoff + jitter."""
    for attempt in range(max_attempts):
        try:
            return fn()
        except (anthropic.RateLimitError, anthropic.APIStatusError):
            if attempt == max_attempts - 1:
                raise
            time.sleep(base * (2 ** attempt) + random.uniform(0, 0.5))

def run_agent(client, registry, system: str, user_msg: str,
              model: str = "claude-sonnet-4-6",
              budget: Budget = Budget()) -> dict:
    messages = [{"role": "user", "content": user_msg}]
    state = RunState()
    log = []                                   # the flight recorder

    while True:
        # 1. The law: budgets checked BEFORE every model turn
        if reason := state.exceeded(budget):
            return {"status": "halted", "reason": reason,
                    "turns": state.turns, "cost": state.cost_usd, "log": log}

        # 2. Flail intervention
        if is_flailing(log):
            last = log[-1]
            messages.append({"role": "user", "content":
                f"You have called {last['tool']} with the same arguments "
                f"3 times with the same result. Do not call it again with "
                f"these arguments. Try a different approach or return a "
                f"FAILURE report."})

        # 3. Call the model (transport retries invisible to it)
        resp = with_retries(lambda: client.messages.create(
            model=model, max_tokens=2048, system=system,
            tools=registry.schemas, messages=messages))
        state.turns += 1
        p = PRICE[model]
        state.cost_usd += (resp.usage.input_tokens  * p["in"]  +
                           resp.usage.output_tokens * p["out"]) / 1_000_000
        messages.append({"role": "assistant", "content": resp.content})

        # 4. Done?
        if resp.stop_reason != "tool_use":
            text = "".join(b.text for b in resp.content if b.type == "text")
            return {"status": "completed", "answer": text,
                    "turns": state.turns, "cost": state.cost_usd, "log": log}

        # 5. Execute every requested tool, log everything
        results = []
        for block in resp.content:
            if block.type == "tool_use":
                t0 = time.monotonic()
                output = registry.execute(block.name, block.input)
                log.append({"turn": state.turns, "tool": block.name,
                            "args": block.input, "result": output[:500],
                            "ms": round((time.monotonic() - t0) * 1000)})
                results.append({"type": "tool_result",
                                "tool_use_id": block.id, "content": output})
        messages.append({"role": "user", "content": results})

def persist_run(result: dict, path="runs.jsonl", workflow="default"):
    record = {"run_id": str(uuid.uuid4()), "workflow": workflow,
              "ts": datetime.datetime.now(datetime.timezone.utc).isoformat(),
              **result}
    with open(path, "a") as f:
        f.write(json.dumps(record) + "\n")
