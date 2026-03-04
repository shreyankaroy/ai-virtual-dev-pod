import os
from dotenv import load_dotenv

load_dotenv()

MODEL_NAME = "llama-3.1-8b-instant"
TEMPERATURE = 0.2
MAX_RETRIES = 3

GROQ_API_KEY = os.getenv("GROQ_API_KEY")