# config/settings.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:

    # ---------------------------
    # LLM CONFIGURATION
    # ---------------------------

    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    MODEL_NAME = os.getenv(
        "MODEL_NAME",
        "llama-3.1-8b-instant"
    )

    TEMPERATURE = float(
        os.getenv("TEMPERATURE", 0.2)
    )

    MAX_RETRIES = int(
        os.getenv("MAX_RETRIES", 5)
    )

    # ---------------------------
    # PATH CONFIGURATION
    # ---------------------------

    BASE_DIR = os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))
    )

    TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

    GENERATED_ARTIFACTS_DIR = os.path.join(
        BASE_DIR,
        "generated_artifacts"
    )

    # ---------------------------
    # SYSTEM CONFIGURATION
    # ---------------------------

    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    REQUEST_TIMEOUT = int(
        os.getenv("REQUEST_TIMEOUT", 30)
    )


# Export easy references
GROQ_API_KEY = Settings.GROQ_API_KEY
MODEL_NAME = Settings.MODEL_NAME
TEMPERATURE = Settings.TEMPERATURE
MAX_RETRIES = Settings.MAX_RETRIES