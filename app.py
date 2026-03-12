from orchestrator.workflow import DevelopmentWorkflow
import json


workflow = DevelopmentWorkflow()

idea = input("Enter product idea: ")

result = workflow.run(idea)

print("\nFINAL OUTPUT\n")

print(json.dumps({
    "idea": result["idea"],
    "artifact_paths": {
        "code": "generated_artifacts/code/",
        "tests": "generated_artifacts/tests/",
        "devops": "generated_artifacts/devops/"
    },
    "test_results": result["test_results"],
    "metrics": result["metrics"]
}, indent=2))