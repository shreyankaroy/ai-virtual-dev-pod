"""Testing Agent — generates pytest test cases for generated code."""

from crewai import Agent


def create_testing_agent(llm):
    """Create the QA Engineer CrewAI agent."""
    return Agent(
        role="QA Engineer",
        goal="Generate comprehensive pytest test cases that validate the generated backend code",
        backstory=(
            "You are a QA engineer who writes thorough test suites covering functionality, "
            "edge cases, and error handling for Python applications."
        ),
        llm=llm,
        verbose=True,
    )