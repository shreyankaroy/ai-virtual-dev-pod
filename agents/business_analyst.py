from agents.base_agent import BaseAgent
from schemas.user_story_schema import UserStoriesOutput
from utils.prompt_loader import load_prompt


class BusinessAnalystAgent(BaseAgent):

    def __init__(self):

        role = "Business Analyst"

        goal = "Convert product ideas into structured user stories."

        backstory = """
You are an expert product analyst who writes clear, actionable user stories.
"""

        super().__init__(role, goal, backstory)

    def generate_user_stories(self, product_idea: str, memory_context=None):

        prompt_template = load_prompt("user_story_prompt.txt")

        prompt = prompt_template.format(product_idea=product_idea,
        memory_context=memory_context)

        return self.run(
            user_input=prompt,
            output_schema=UserStoriesOutput
        )