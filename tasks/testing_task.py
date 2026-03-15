"""Testing task."""

from crewai import Task


def create_testing_task(agent, code_output):
    """Create a task for generating pytest test cases from generated code."""
    return Task(
        description=(
            f"Based on the following generated code, write pytest test cases.\n\n"
            f"GENERATED CODE:\n{code_output}\n\n"
            f"Generate:\n"
            f"1. test_api.py - API endpoint tests using FastAPI TestClient\n"
            f"2. test_services.py - Unit tests for service functions\n"
            f"3. test_report.md - Brief summary of what is tested\n\n"
            f"Rules:\n"
            f"- Use pytest framework\n"
            f"- Use FastAPI TestClient for API tests\n"
            f"- Test both success and error cases\n"
            f"- Include clear test names"
        ),
        expected_output=(
            "Complete pytest files (test_api.py, test_services.py) "
            "and a test_report.md summarizing test coverage."
        ),
        agent=agent,
    )
