"""Chapter 4 — the tool registry. Schemas generated from typed functions."""
import inspect, json
from typing import get_type_hints

PY_TO_JSON = {str: "string", int: "integer", float: "number", bool: "boolean"}

class ToolRegistry:
    def __init__(self):
        self._tools = {}          # name -> (function, schema)

    def register(self, fn):
        """Decorator: turns a typed Python function into a tool."""
        hints = get_type_hints(fn)
        hints.pop("return", None)
        sig = inspect.signature(fn)
        props, required = {}, []
        for pname, param in sig.parameters.items():
            props[pname] = {"type": PY_TO_JSON[hints[pname]]}
            if param.default is inspect.Parameter.empty:
                required.append(pname)
        schema = {
            "name": fn.__name__,
            "description": inspect.getdoc(fn) or "",
            "input_schema": {"type": "object",
                             "properties": props, "required": required},
        }
        self._tools[fn.__name__] = (fn, schema)
        return fn

    @property
    def schemas(self):
        return [s for _, s in self._tools.values()]

    def execute(self, name: str, args: dict) -> str:
        """Run a tool by name. Never raises — always returns a string."""
        if name not in self._tools:
            return json.dumps({"error": "unknown_tool",
                               "known_tools": list(self._tools)})
        fn, _ = self._tools[name]
        try:
            return str(fn(**args))
        except TypeError as e:
            return json.dumps({"error": "bad_arguments", "message": str(e)})
        except Exception as e:
            return json.dumps({"error": "tool_exception",
                               "type": type(e).__name__, "message": str(e)})
