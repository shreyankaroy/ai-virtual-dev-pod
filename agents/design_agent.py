"""Design Agent — generates system architecture from user stories."""

from crewai import Agent


def create_design_agent(llm):
    """Create the System Architect CrewAI agent."""
    return Agent(
        role="System Architect",
        goal="Design system architecture, API specifications, and database schemas from user stories",
        backstory=(
            "You are a senior system architect who designs scalable, production-ready software systems. "
            "You create clear component diagrams, API contracts, and data models."
        ),
        llm=llm,
        verbose=True,
    )
