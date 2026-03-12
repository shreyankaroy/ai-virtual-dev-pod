from groq import Groq
from config.settings import Settings
from utils.json_validator import validate_json_structure
from utils.logger import log
import time


class BaseAgent:

    def __init__(self, role: str, goal: str, backstory: str):

        self.role = role
        self.goal = goal
        self.backstory = backstory
        self.client = Groq(api_key=Settings.GROQ_API_KEY)

    def _build_system_prompt(self) -> str:

        return f"""
You are a {self.role}.

Your goal:
{self.goal}

Context:
{self.backstory}

Strict Rules:
- Return ONLY valid JSON.
- Do not include explanations.
- Do not include markdown.
- Do not include text outside JSON.
- Use ONLY single quotes in any Python code you generate.
- NEVER use triple quotes in generated code.

Code Architecture Rules:
- Never create circular imports.
- models.py must NEVER import api.py.
- api.py may import models.py.
- service.py may import models.py.
- Tests may import everything.
- Always use absolute imports.
Code Architecture Rules:
- Never create circular imports.
- models.py must NEVER import api.py.
- api.py may import models.py.
- service.py may import models.py.
- Tests may import everything.
- Always use absolute imports.
"""

    def _clean_output(self, text: str) -> str:
        """
        Clean common JSON-breaking patterns from LLM outputs.
        """

        if not text:
            return ""

        # remove markdown blocks
        text = text.replace("```json", "")
        text = text.replace("```python", "")
        text = text.replace("```", "")

        # remove triple quotes
        text = text.replace('"""', "'")

        return text.strip()

    def run(self, user_input: str, output_schema=None):

        system_prompt = self._build_system_prompt()

        for attempt in range(Settings.MAX_RETRIES):

            try:

                log.info(f"{self.role} attempt {attempt + 1}")

                # rough token estimate
                approx_tokens = int((len(system_prompt) + len(user_input)) / 4)
                log.info(f"{self.role} prompt size ≈ {approx_tokens} tokens")

                response = self.client.chat.completions.create(
                    model=Settings.MODEL_NAME,
                    temperature=Settings.TEMPERATURE,
                    response_format={"type": "json_object"},
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_input},
                    ],
                )

                output_text = response.choices[0].message.content

                if not output_text:
                    log.warning(f"{self.role} returned empty output")
                    continue

                output_text = self._clean_output(output_text)

                valid, result = validate_json_structure(
                    output_text,
                    schema=output_schema
                )

                if valid:
                    log.success(f"{self.role} produced valid output")
                    return result

                else:
                    log.warning(f"{self.role} returned invalid JSON")

            except Exception as e:

                error_str = str(e)

                # Daily quota exceeded
                if "tokens per day" in error_str or "TPD" in error_str:
                    log.error("Daily token limit exhausted.")
                    raise SystemExit(1)

                # Rate limit
                elif "429" in error_str or "rate_limit_exceeded" in error_str:

                    wait_time = min(2 ** (attempt + 1), 30)

                    log.warning(
                        f"{self.role} hit rate limit. "
                        f"Retrying in {wait_time} seconds..."
                    )

                    time.sleep(wait_time)

                else:
                    log.error(f"{self.role} error: {error_str}")

        raise ValueError(
            f"{self.role} failed after {Settings.MAX_RETRIES} attempts."
        )