from agents.base_agent import BaseAgent
from utils.prompt_loader import load_template

class BusinessAnalystAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            role="Business Analyst",
            goal="Convert high-level business requirements into structured epics and user stories.",
            backstory="You work in an IT organization and follow strict documentation standards."
        )

    def generate_user_stories(self, requirement: str):
        template = load_template("templates/user_story_template.txt")

        prompt = f"""
Business Requirement:
{requirement}

Follow this template strictly:
{template}
"""

        required_keys = ["epics", "user_stories", "acceptance_criteria"]

        return self.run(prompt, required_keys)