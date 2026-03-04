from agents.business_analyst import BusinessAnalystAgent
import json
import os

if __name__ == "__main__":
    agent = BusinessAnalystAgent()

    requirement = "Build a food delivery backend with user authentication and order tracking."

    result = agent.generate_user_stories(requirement)

    print(result)

    # create folder if it doesn't exist
    os.makedirs("generated_artifacts", exist_ok=True)

    # save output
    with open("generated_artifacts/user_stories.json", "w") as f:
        json.dump(result, f, indent=2)

    print("User stories saved to generated_artifacts/user_stories.json")