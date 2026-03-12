from agents.base_agent import BaseAgent
from schemas.debug_schema import DebugOutput
from utils.prompt_loader import load_prompt
import json
import re


class DebugAgent(BaseAgent):

    def __init__(self):
        role = "Debug Engineer"
        goal = "Fix failing code based on test errors."
        backstory = """
You are an expert Python engineer who fixes bugs in backend systems.
"""
        super().__init__(role, goal, backstory)

    def _compress_test_output(self, test_output: str) -> str:
        """Extract only FAILED lines and error messages, drop full tracebacks."""
        lines = test_output.split('\n')
        compressed = []
        for line in lines:
            # Keep failure summary lines and actual error lines only
            if any(x in line for x in [
                'FAILED', 'ERROR', 'AssertionError',
                'NameError', 'ImportError', 'ModuleNotFoundError',
                'TypeError', 'short test summary'
            ]):
                compressed.append(line.strip())
        return '\n'.join(compressed[:30])  # cap at 30 lines max

    def fix_code(self, code_plan, failing_tests):

        prompt_template = load_prompt("debug_prompt.txt")

        # Handle both dict with 'files' key and raw list
        if isinstance(code_plan, dict):
            files = code_plan.get('files', [])
        else:
            files = code_plan

        from utils.compressor import compress_design
        
        prompt = prompt_template.format(
            code_plan=json.dumps(files),
            failing_tests=failing_tests
        )

        return self.run(
            user_input=prompt,
            output_schema=DebugOutput
        )

        # Compress test output — only keep error lines
        compressed_tests = self._compress_test_output(str(failing_tests))

        prompt = prompt_template.format(
            code_plan=json.dumps(compressed_code),
            failing_tests=compressed_tests
        )

        return self.run(
            user_input=prompt,
            output_schema=DebugOutput
        )
