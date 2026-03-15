"""Developer Agent — generates backend code from design documents."""

from crewai import Agent


def create_developer(llm):
    """Create the Developer CrewAI agent."""
    return Agent(
        role="Senior Software Developer",
        goal="Generate clean, modular Python backend code based on design documents and user stories",
        backstory=(
            "You are a senior Python developer who writes well-structured backend code. "
            "You follow best practices including separation of concerns, proper error handling, "
            "and clear documentation."
        ),
        llm=llm,
        verbose=True,
    )