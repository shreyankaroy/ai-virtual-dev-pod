import os
from utils.logger import log


def apply_debug_fixes(debug_output):

    for file in debug_output["files"]:

        filename = file["filename"]

        # Allow patching both code and test files
        if filename.startswith("generated_artifacts/code") or filename.startswith("generated_artifacts/tests"):
            normalized = filename
        elif "test_" in filename:
            normalized = os.path.join("generated_artifacts", "tests", os.path.basename(filename))
        else:
            normalized = os.path.join("generated_artifacts", "code", os.path.basename(filename))

        os.makedirs(os.path.dirname(normalized), exist_ok=True)

        with open(normalized, "w") as f:
            f.write(file["code"])

        log.info(f"Patched file: {normalized}")

    log.success("Debug fixes applied")