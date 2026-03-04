from groq import Groq
from config.settings import MODEL_NAME, TEMPERATURE, MAX_RETRIES, GROQ_API_KEY
from utils.json_validator import validate_json_structure

class BaseAgent:
    def __init__(self, role: str, goal: str, backstory: str):
        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.client = Groq(api_key=GROQ_API_KEY)

    def _build_system_prompt(self):
        return f"""
You are a {self.role}.
Goal: {self.goal}
Context: {self.backstory}

Return ONLY valid JSON.
Do not include explanations.
"""

    def run(self, user_input: str, required_keys: list):
        system_prompt = self._build_system_prompt()

        for attempt in range(MAX_RETRIES):

            response = self.client.chat.completions.create(
                model=MODEL_NAME,
                temperature=TEMPERATURE,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
            )

            output_text = response.choices[0].message.content.strip()

            valid, result = validate_json_structure(output_text, required_keys)

            if valid:
                return result

        raise ValueError("Failed to produce valid JSON after retries.")