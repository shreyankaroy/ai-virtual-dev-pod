"""Code generation task."""

from crewai import Task


def create_dev_task(agent, user_stories, design):
    """Create a task for generating backend code from design and user stories."""
    return Task(
        description=(
            f"Based on the following design and user stories, generate Python backend code.\n\n"
            f"USER STORIES:\n{user_stories}\n\n"
            f"SYSTEM DESIGN:\n{design}\n\n"
            f"Generate these files (output each with a clear '## filename' header):\n"
            f"1. app.py - FastAPI application with routes\n"
            f"2. models.py - Pydantic data models\n"
            f"3. services.py - Business logic layer\n"
            f"4. requirements.txt - Python dependencies\n\n"
            f"Rules:\n"
            f"- Use FastAPI and Pydantic\n"
            f"- Keep code clean and modular with docstrings\n"
            f"- No database connections, use in-memory storage\n"
            f"- Use regular def (no async)"
        ),
        expected_output=(
            "Complete Python source code for app.py, models.py, services.py, "
            "and requirements.txt, each clearly separated with filename headers."
        ),
        agent=agent,
    )
