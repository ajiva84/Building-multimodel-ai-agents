"""Chapter 2 — the adapter layer. The ONLY file that imports provider SDKs."""
import anthropic

_clients = {}

def _anthropic():
    return _clients.setdefault("anthropic", anthropic.Anthropic())

def _gemini():
    from google import genai
    return _clients.setdefault("gemini", genai.Client())

def complete(model: str, system: str, messages: list,
             tools: list | None = None, max_tokens: int = 2048):
    """model = 'provider/name', e.g. 'anthropic/claude-sonnet-4-6'
    Returns a normalized dict: {text, tool_calls, stop, usage}"""
    provider, name = model.split("/", 1)
    if provider == "anthropic":
        r = _anthropic().messages.create(
            model=name, system=system, messages=messages,
            tools=tools or [], max_tokens=max_tokens)
        return {
            "text": "".join(b.text for b in r.content if b.type == "text"),
            "tool_calls": [{"id": b.id, "name": b.name, "args": b.input}
                           for b in r.content if b.type == "tool_use"],
            "stop": r.stop_reason,
            "usage": {"in": r.usage.input_tokens, "out": r.usage.output_tokens},
        }
    if provider == "google":
        # STUB: translate to Gemini's format, call, normalize back to the
        # exact same shape as above. Chapter 2 exercise.
        raise NotImplementedError("Gemini branch — see Chapter 2")
    raise ValueError(f"unknown provider: {provider}")
