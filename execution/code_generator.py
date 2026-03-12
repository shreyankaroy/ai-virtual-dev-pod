import os
from utils.logger import log


CODE_DIR = "generated_artifacts/code"


def generate_code_files(code_plan):

    os.makedirs(CODE_DIR, exist_ok=True)

    files = code_plan.get("files", [])

    for file in files:

        filename = file["filename"]
        code = file["code"]

        path = os.path.join(CODE_DIR, filename)

        with open(path, "w") as f:
            f.write(code)

        log.info(f"Generated file: {filename}")

    log.success("Code files generated successfully")