import os

def save_generated_files(files):

    os.makedirs("generated_code", exist_ok=True)

    for file in files:
        path = os.path.join("generated_code", file["filename"])

        with open(path, "w", encoding="utf-8") as f:
            f.write(file["content"])