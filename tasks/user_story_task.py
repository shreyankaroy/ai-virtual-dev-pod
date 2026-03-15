"""User story generation task."""

from crewai import Task


def create_user_story_task(agent, requirement):
    """Create a task for generating user stories from a business requirement."""
    return Task(
        description=(
            f"Analyze this business requirement and generate detailed user stories.\n\n"
            f"REQUIREMENT: {requirement}\n\n"
            f"Generate 4-6 user stories. Each must have:\n"
            f"- A clear title\n"
            f"- Description in 'As a [user], I want [feature] so that [benefit]' format\n"
            f"- 3-5 acceptance criteria\n\n"
            f"Format as a well-structured markdown document."
        ),
        expected_output=(
            "A markdown document containing 4-6 structured user stories "
            "with titles, descriptions, and acceptance criteria."
        ),
        agent=agent,
    )
