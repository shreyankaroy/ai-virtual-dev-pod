from agents.base_agent import BaseAgent
from schemas.system_design_schema import SystemDesignOutput
from utils.prompt_loader import load_prompt
from utils.compressor import compress_stories


class SystemDesignerAgent(BaseAgent):

    def __init__(self):
        role = "System Architect"
        goal = "Design system architecture from user stories."
        backstory = """
You are a senior system architect skilled at converting product requirements
into scalable software architectures.
"""
        super().__init__(role, goal, backstory)

    def design_system(self, user_stories, memory_context=None):

        prompt_template = load_prompt("system_design_prompt.txt")

        # Compress stories instead of dumping full JSON
        compressed = compress_stories(user_stories)

        prompt = prompt_template.format(
            user_stories=compressed,
            memory_context=memory_context or "None"
        )

        return self.run(
            user_input=prompt,
            output_schema=SystemDesignOutput
        )