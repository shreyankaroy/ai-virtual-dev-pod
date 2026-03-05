from agents.base_agent import BaseAgent
from utils.prompt_loader import load_template

class DeveloperAgent(BaseAgent):

    def __init__(self):

        role = "Senior Backend Developer"

        goal = """
Generate working backend code based on system design
and user stories.
"""

        backstory = """
You are a senior backend engineer who writes clean,
modular, production-ready Python backend code.
"""

        super().__init__(role, goal, backstory)

    def generate_code(self, design_document: str):

        code_template = load_template("templates/code_template.txt")

        prompt = f"""
Using the following system design:

{design_document}

Generate backend code.

Follow this template:

{code_template}
"""

        required_keys = [
            "files"
        ]

        return self.run(prompt, required_keys)