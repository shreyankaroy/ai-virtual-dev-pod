from agents.base_agent import BaseAgent
from schemas.devops_schema import DevOpsOutput
from utils.prompt_loader import load_prompt
import json


class DevOpsAgent(BaseAgent):

    def __init__(self):

        role = "DevOps Engineer"

        goal = "Generate deployment configuration and infrastructure files."

        backstory = """
You are a senior DevOps engineer who prepares applications for deployment.
You create Dockerfiles, requirements files, and project documentation.
"""

        super().__init__(role, goal, backstory)

    def generate_devops(self, code_plan):

        prompt_template = load_prompt("devops_prompt.txt")

        prompt = prompt_template.format(
            code_plan=json.dumps(code_plan)
        )

        return self.run(
            user_input=prompt,
            output_schema=DevOpsOutput
        )