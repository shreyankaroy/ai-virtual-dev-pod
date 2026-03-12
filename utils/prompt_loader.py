# utils/prompt_loader.py

import os
from config.settings import Settings
from utils.logger import log


def load_prompt(template_name: str):
    """
    Load prompt template from templates folder.
    """

    template_path = os.path.join(
        Settings.TEMPLATE_DIR,
        template_name
    )

    if not os.path.exists(template_path):

        log.error(f"Prompt template not found: {template_name}")
        raise FileNotFoundError(
            f"Template {template_name} not found"
        )

    with open(template_path, "r", encoding="utf-8") as file:

        prompt = file.read()

    return prompt