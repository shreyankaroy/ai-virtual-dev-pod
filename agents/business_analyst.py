"""Business Analyst agent — generates user stories from requirements."""

from crewai import Agent


def create_business_analyst(llm):
    """Create the Business Analyst CrewAI agent."""
    return Agent(
        role="Business Analyst",
        goal="Convert business requirements into detailed user stories with acceptance criteria",
        backstory=(
            "You are a senior product analyst with deep experience in agile development. "
            "You write clear, actionable user stories that development teams can implement directly."
        ),
        llm=llm,
        verbose=True,
    )