"""Chapter 1 — a complete agent in ~50 lines."""
import anthropic, json

client = anthropic.Anthropic()          # reads ANTHROPIC_API_KEY

def get_weather(city: str) -> str:      # stub — imagine a real API
    return json.dumps({"city": city, "temp_f": 93, "conditions": "humid"})

TOOLS = [{
    "name": "get_weather",
    "description": "Get current weather for a city.",
    "input_schema": {"type": "object",
                     "properties": {"city": {"type": "string"}},
                     "required": ["city"]},
}]
IMPL = {"get_weather": get_weather}

def run_agent(user_message: str, max_turns: int = 5) -> str:
    messages = [{"role": "user", "content": user_message}]
    for _ in range(max_turns):                      # the leash
        resp = client.messages.create(
            model="claude-sonnet-4-6", max_tokens=1024,
            system="You are a helpful assistant. Use tools when needed.",
            tools=TOOLS, messages=messages)
        messages.append({"role": "assistant", "content": resp.content})
        if resp.stop_reason != "tool_use":          # model is done talking
            return "".join(b.text for b in resp.content if b.type == "text")
        results = []
        for block in resp.content:                  # execute what it asked for
            if block.type == "tool_use":
                out = IMPL[block.name](**block.input)
                results.append({"type": "tool_result",
                                "tool_use_id": block.id, "content": out})
        messages.append({"role": "user", "content": results})
    return "Agent hit turn limit."

if __name__ == "__main__":
    print(run_agent("Should I wear a jacket in Houston today?"))
