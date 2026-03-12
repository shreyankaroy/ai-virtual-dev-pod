import os
from utils.logger import log


def generate_test_files(test_plan):

    base_path = "generated_artifacts/tests"
    os.makedirs(base_path, exist_ok=True)

    for file in test_plan["files"]:
        path = os.path.join(base_path, file["filename"])

        with open(path, "w") as f:
            f.write(file["code"])

        log.info(f"Generated test file: {file['filename']}")

    log.success("Test files generated successfully")