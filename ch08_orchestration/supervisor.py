"""Chapter 8 — the supervisor: workers are just tools."""
import sys
sys.path += ["../ch04_tools", "../ch05_loop"]
from registry import ToolRegistry
from loop import run_agent, Budget

def make_worker_tool(registry: ToolRegistry, client, worker_registry,
                     worker_prompt: str, name: str, doc: str):
    """Wrap a whole agent as a tool the supervisor can call.
    Every worker gets its OWN budget — non-negotiable."""
    def worker(question: str) -> str:
        result = run_agent(client, worker_registry,
                           system=worker_prompt, user_msg=question,
                           budget=Budget(max_turns=6, max_cost_usd=0.10))
        return result.get("answer", f"WORKER FAILED: {result.get('reason')}")
    worker.__name__ = name
    worker.__doc__ = doc
    registry.register(worker)
