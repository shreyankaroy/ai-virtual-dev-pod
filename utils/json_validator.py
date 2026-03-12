import json
from utils.logger import log


def normalize_test_output(data):
    """
    Fix common LLM mistakes in test output.
    Converts dict expected_result into string.
    """

    if isinstance(data, dict) and "test_cases" in data:
        for case in data["test_cases"]:
            if isinstance(case.get("expected_result"), dict):
                case["expected_result"] = json.dumps(case["expected_result"])

    return data


def validate_json_structure(output_text: str, schema=None):
    """
    Validate JSON output and optionally validate against a schema.

    Returns:
        (True, parsed_output) if valid
        (False, error_message) if invalid
    """

    try:
        parsed = json.loads(output_text)

        # FIX LLM STRUCTURE ISSUES
        parsed = normalize_test_output(parsed)

    except json.JSONDecodeError as e:
        log.warning("Invalid JSON returned by LLM")
        return False, f"Invalid JSON: {str(e)}"

    if schema:
        try:
            validated = schema.model_validate(parsed)
            return True, validated.model_dump()
        except Exception as e:
            log.warning(f"Schema validation failed: {str(e)}")
            return False, str(e)

    return True, parsed