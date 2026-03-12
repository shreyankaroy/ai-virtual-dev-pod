import os
from utils.logger import log


def generate_devops_files(devops_output):

    output_dir = "generated_artifacts/devops"

    os.makedirs(output_dir, exist_ok=True)

    for file in devops_output["files"]:

        path = os.path.join(output_dir, file["filename"])

        with open(path, "w", encoding="utf-8") as f:
            f.write(file["content"])

        log.info(f"Generated DevOps file: {file['filename']}")

    log.success("DevOps artifacts generated successfully")