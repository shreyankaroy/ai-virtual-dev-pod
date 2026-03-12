import os


def load_generated_code():

    code_dir = "generated_artifacts/code"

    code_contents = {}

    if not os.path.exists(code_dir):
        return code_contents

    for file in os.listdir(code_dir):

        if file.endswith(".py"):

            path = os.path.join(code_dir, file)

            with open(path, "r", encoding="utf-8") as f:
                code_contents[file] = f.read()

    return code_contents