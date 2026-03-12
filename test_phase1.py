from config.settings import Settings
from utils.logger import log
from utils.json_validator import validate_json
from utils.prompt_loader import load_prompt
from agents.base_agent import BaseAgent


print("Settings loaded:", Settings.MODEL_NAME)

log.info("Logger working!")

sample_json = '{"name": "test"}'
print("JSON validation:", validate_json(sample_json))

print("All imports successful!")