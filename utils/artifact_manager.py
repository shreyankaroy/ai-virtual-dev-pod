"""
Artifact manager — saves JSON artifacts, generates markdown reports,
and embeds summaries into ChromaDB vector memory.
"""

import json
import os
from utils.logger import log


ARTIFACT_DIR = "generated_artifacts"
PROJECT_ARTIFACTS_DIR = "project_artifacts"


def save_artifact(filename, data):
    """Save a JSON artifact and also generate markdown + embed into ChromaDB."""

    # 1. Save raw JSON artifact
    os.makedirs(ARTIFACT_DIR, exist_ok=True)
    path = os.path.join(ARTIFACT_DIR, filename)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
    log.info(f"Saved artifact: {path}")

    # 2. Generate markdown artifact
    _save_markdown(filename, data)

    # 3. Embed into vector memory
    _embed_artifact(filename, data)


def _save_markdown(filename, data):
    """Generate a readable markdown file from the artifact data."""
    os.makedirs(PROJECT_ARTIFACTS_DIR, exist_ok=True)

    base = filename.replace(".json", "")
    md_path = os.path.join(PROJECT_ARTIFACTS_DIR, f"{base}.md")

    try:
        if "user_stories" in filename:
            md = _format_user_stories(data)
        elif "architecture" in filename:
            md = _format_architecture(data)
        elif "code_plan" in filename:
            md = _format_code_plan(data)
        elif "test_plan" in filename:
            md = _format_test_plan(data)
        elif "devops" in filename:
            md = _format_devops(data)
        else:
            md = f"# {base}\n\n```json\n{json.dumps(data, indent=2)}\n```\n"

        with open(md_path, "w") as f:
            f.write(md)
        log.info(f"Saved markdown artifact: {md_path}")

    except Exception as e:
        log.warning(f"Markdown generation failed for {filename}: {e}")


def _embed_artifact(filename, data):
    """Embed a text summary of the artifact into ChromaDB."""
    try:
        from memory.vectordb import get_vector_memory
        vm = get_vector_memory()

        # Build a compact text summary for embedding
        summary = json.dumps(data, indent=1)[:4000]
        vm.add(
            doc_id=filename.replace(".json", ""),
            text=summary,
            metadata={"source": filename}
        )
    except Exception as e:
        log.warning(f"Vector embedding failed for {filename}: {e}")


# ── Markdown formatters ──────────────────────────────────────────


def _format_user_stories(data):
    lines = ["# User Stories\n"]
    stories = data.get("stories", [])
    for i, s in enumerate(stories, 1):
        lines.append(f"## Story {i}: {s.get('title', 'Untitled')}\n")
        lines.append(f"{s.get('description', '')}\n")
        lines.append("### Acceptance Criteria\n")
        for ac in s.get("acceptance_criteria", []):
            lines.append(f"- {ac}")
        lines.append("")
    return "\n".join(lines)


def _format_architecture(data):
    lines = ["# System Architecture\n"]
    lines.append(f"## Summary\n{data.get('architecture_summary', 'N/A')}\n")

    lines.append("## Components\n")
    for c in data.get("components", []):
        lines.append(f"- **{c.get('name', '')}**: {c.get('description', '')}")
    lines.append("")

    lines.append("## Data Flow\n")
    for d in data.get("data_flow", []):
        lines.append(
            f"- {d.get('source', '')} → {d.get('target', '')}: "
            f"{d.get('description', '')}"
        )
    lines.append("")
    return "\n".join(lines)


def _format_code_plan(data):
    lines = ["# Generated Code Plan\n"]
    for f in data.get("files", []):
        lines.append(f"## {f.get('filename', 'unknown')}\n")
        lines.append(f"{f.get('description', '')}\n")
        lines.append(f"```python\n{f.get('code', '')}\n```\n")
    return "\n".join(lines)


def _format_test_plan(data):
    lines = ["# Test Plan\n"]
    for f in data.get("files", []):
        lines.append(f"## {f.get('filename', 'unknown')}\n")
        lines.append(f"{f.get('description', '')}\n")
        lines.append(f"```python\n{f.get('code', '')}\n```\n")
    return "\n".join(lines)


def _format_devops(data):
    lines = ["# DevOps Artifacts\n"]
    for f in data.get("files", []):
        lines.append(f"## {f.get('filename', 'unknown')}\n")
        lines.append(f"{f.get('description', '')}\n")
        lines.append(f"```\n{f.get('content', '')}\n```\n")
    return "\n".join(lines)