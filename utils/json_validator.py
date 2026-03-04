import json

def validate_json_structure(response_text: str, required_keys: list):
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        return False, "Invalid JSON format"

    for key in required_keys:
        if key not in data:
            return False, f"Missing key: {key}"

    return True, data