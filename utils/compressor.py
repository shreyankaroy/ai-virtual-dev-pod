def compress_stories(stories):
    """Convert full user story objects into compact single-line strings."""
    return "\n".join(
        f"- {s['title']}: {s['description']}"
        for s in stories
    )

def compress_design(system_design):
    """Send only summary + component names instead of full design JSON."""
    summary = system_design.get("architecture_summary", "")
    components = "\n".join(
        f"- {c['name']}: {c['description']}"
        for c in system_design.get("components", [])
    )
    return f"{summary}\nComponents:\n{components}"