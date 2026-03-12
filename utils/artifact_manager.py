import json
import os


ARTIFACT_DIR = "generated_artifacts"


def save_artifact(filename, data):

    os.makedirs(ARTIFACT_DIR, exist_ok=True)

    path = os.path.join(ARTIFACT_DIR, filename)

    with open(path, "w") as f:
        json.dump(data, f, indent=2)