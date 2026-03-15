"""
Artifact manager — saves generated artifacts to structured directories.
"""

import os

BASE_DIR = "project_artifacts"


def save_artifact(relative_path: str, content: str):
    """Save content to a file under project_artifacts/."""
    full_path = os.path.join(BASE_DIR, relative_path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  📄 Saved: {full_path}")
    return full_path


def load_artifact(relative_path: str) -> str:
    """Load content from a saved artifact."""
    full_path = os.path.join(BASE_DIR, relative_path)
    if not os.path.exists(full_path):
        return ""
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()
