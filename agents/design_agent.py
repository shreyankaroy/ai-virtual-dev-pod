from agents.base_agent import BaseAgent
from utils.prompt_loader import load_template

class DesignAgent(BaseAgent):

    def __init__(self):

        role = "Software Architect"

        goal = """
Design the technical architecture of the software
based on the user stories provided.
"""

        backstory = """
You are an experienced software architect who designs scalable
backend systems. You translate product requirements into system
architecture, database schema, and API specifications.
"""

        super().__init__(role, goal, backstory)

    def generate_design(self, user_stories: str):

        design_template = load_template("templates/design_template.txt")

        prompt = f"""
Using the following user stories:

{user_stories}

Generate a complete system design.

Follow this template:

{design_template}
"""

        required_keys = [
            "architecture_overview",
            "tech_stack",
            "database_schema",
            "api_contracts"
        ]

        return self.run(prompt, required_keys)