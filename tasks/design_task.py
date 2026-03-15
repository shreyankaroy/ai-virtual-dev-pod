"""System design task."""

from crewai import Task


def create_design_task(agent, user_stories):
    """Create a task for generating system design from user stories."""
    return Task(
        description=(
            f"Based on the following user stories, create a system design document.\n\n"
            f"USER STORIES:\n{user_stories}\n\n"
            f"Include:\n"
            f"1. Architecture summary\n"
            f"2. Component descriptions with responsibilities\n"
            f"3. API endpoint specifications (method, path, description)\n"
            f"4. Database entity definitions with fields\n"
            f"5. Data flow between components\n\n"
            f"Format as a well-structured markdown document."
        ),
        expected_output=(
            "A markdown document with system architecture, "
            "API specs, database schema, and data flow."
        ),
        agent=agent,
    )
