"""Chapter 8 — the router: a cheap receptionist."""

def make_router(client, routes: dict):
    """routes: {"label": agent_callable, ..., "other": fallback_callable}"""
    assert "other" in routes, "always include an 'other' escape route"

    def route(task: str):
        label = client.messages.create(
            model="claude-haiku-4-5-20251001",     # cheap tier — easy work
            max_tokens=10,
            system=("Classify the task into exactly one of: "
                    + ", ".join(routes) + ". Reply with only the label."),
            messages=[{"role": "user", "content": task}],
        ).content[0].text.strip()
        return routes.get(label, routes["other"])(task)

    return route
