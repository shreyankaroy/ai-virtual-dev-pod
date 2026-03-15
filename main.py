"""
AI-Powered Virtual Development Pod — CLI Entry Point
=====================================================
Usage:  python main.py
"""

from agents.project_lead import ProjectLead


def main():
    print("\n🤖 AI-Powered Virtual Development Pod")
    print("=" * 50)

    requirement = input("\nEnter your project requirement:\n> ").strip()

    if not requirement:
        print("No requirement entered. Exiting.")
        return

    print(f"\n🚀 Starting pipeline for: {requirement}\n")

    lead = ProjectLead()
    results = lead.run(requirement)

    print("\n" + "=" * 50)
    print("✅ Pipeline Complete!")
    print("=" * 50)

    print("\n📦 Artifacts saved to project_artifacts/")
    print("  • requirements/user_stories.md")
    print("  • design/architecture.md")
    print("  • code/backend/generated_code.md")
    print("  • tests/test_cases.md")

    print("\n📡 Communication Log:")
    for entry in results.get("comm_log", []):
        print(f"  {entry}")


if __name__ == "__main__":
    main()
