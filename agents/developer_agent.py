from agents.base_agent import BaseAgent
from schemas.code_schema import CodeOutput
from utils.prompt_loader import load_prompt
from utils.compressor import compress_design


class DeveloperAgent(BaseAgent):

    def __init__(self):
        role = "Software Developer"
        goal = "Generate production-ready code from system design."
        backstory = """
You are a senior software engineer who writes clean, modular Python code following best practices.
"""
        super().__init__(role, goal, backstory)

    def generate_code(self, system_design, memory_context=None):

        prompt_template = load_prompt("code_prompt.txt")

        # Send only compressed summary instead of full system design JSON
        compressed = compress_design(system_design)

        prompt = prompt_template.format(
            system_design=compressed,
            memory_context=memory_context or "None"
        )

        return self.run(
            user_input=prompt,
            output_schema=CodeOutput
        )

    def fix_code(self, system_design, failing_tests):

        prompt_template = load_prompt("code_fix_prompt.txt")

        compressed = compress_design(system_design)

        prompt = prompt_template.format(
            system_design=compressed,
            failing_tests=failing_tests
        )

        return self.run(
            user_input=prompt,
            output_schema=CodeOutput
        )