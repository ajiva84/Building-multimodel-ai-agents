"""Chapter 2 — structured output: ask, validate, repair."""
import json
from llm import complete

def get_structured(model: str, system: str, prompt: str,
                   validate, max_repairs: int = 2) -> dict | None:
    """validate(data) returns a list of error strings ([] means valid)."""
    messages = [{"role": "user", "content": prompt}]
    for _ in range(max_repairs + 1):
        r = complete(model, system, messages, max_tokens=1024)
        raw = r["text"].strip().removeprefix("```json").removesuffix("```")
        try:
            data = json.loads(raw)
            errors = validate(data)
            if not errors:
                return data
            problem = f"Validation failed: {errors}"
        except json.JSONDecodeError as e:
            problem = f"Invalid JSON: {e}"
        messages += [{"role": "assistant", "content": r["text"]},
                     {"role": "user", "content":
                      f"{problem}\nReply with ONLY the corrected JSON."}]
    return None    # caller escalates (bigger model, or human)
