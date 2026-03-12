from agents.base_agent import BaseAgent
from schemas.test_schema import TestOutput
from utils.prompt_loader import load_prompt
from utils.code_loader import load_generated_code
from utils.compressor import compress_design
import json


class TestingAgent(BaseAgent):

    def __init__(self):
        role = "QA Engineer"
        goal = "Generate test cases to validate the generated code."
        backstory = """
You are a QA engineer skilled at writing clear functional test cases.
"""
        super().__init__(role, goal, backstory)

    def generate_tests(self, system_design, code_plan):

        generated_code = load_generated_code()

        prompt_template = load_prompt("test_prompt.txt")

        # Compress system_design instead of full JSON
        compressed_design = compress_design(system_design)

        # Extract only filenames and descriptions from code_plan, not full code
        compressed_code_plan = [
            {"filename": f["filename"], "description": f["description"]}
            for f in code_plan.get("files", [])
        ]

        prompt = prompt_template.format(
            system_design=compressed_design,
            code_plan=json.dumps(compressed_code_plan),
            generated_code=json.dumps(generated_code)
        )

        return self.run(
            user_input=prompt,
            output_schema=TestOutput
        )