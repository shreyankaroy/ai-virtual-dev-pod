from agents.business_analyst import BusinessAnalystAgent

agent = BusinessAnalystAgent()

result = agent.generate_user_stories(
    "An AI fitness trainer app that adapts workouts based on injuries and travel."
)

print("\nRESULT:\n")
print(result)