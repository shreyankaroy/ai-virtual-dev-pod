import subprocess
import os
from utils.logger import log


def run_tests():

    try:
        env = os.environ.copy()

        code_path = os.path.abspath("generated_artifacts/code")
        existing = env.get("PYTHONPATH", "")
        env["PYTHONPATH"] = f"{code_path}{os.pathsep}{existing}" if existing else code_path

        result = subprocess.run(
            ["pytest", "generated_artifacts/tests", "-v"],
            capture_output=True,
            text=True,
            env=env
        )

        output = result.stdout + result.stderr

        if result.returncode == 0:
            log.success("All tests passed")
            return True, output

        log.warning("Tests failed")
        log.warning(result.stdout)

        return False, output

    except Exception as e:
        log.error(f"Test execution failed: {e}")
        return False, str(e)