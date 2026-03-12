def decide_next_agent(state):
    """
    Decide which agent should run next based on project state.
    """

    if state["user_stories"] is None:
        return "business_analyst"

    if state["system_design"] is None:
        return "system_designer"

    if state["code_plan"] is None:
        return "developer"

    if state["tests"] is None:
        return "tester"

    if state["test_results"] == "fail":
        return "debugger"

    if state["test_results"] == "pass" and state["devops"] is None:
        return "devops"


    return "complete"