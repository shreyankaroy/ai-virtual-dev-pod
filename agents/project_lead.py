"""
Project Lead Agent — orchestrates the full AI development pipeline.
Runs each agent step-by-step using CrewAI, saving artifacts and updating status.
"""

import os
import time
from dotenv import load_dotenv
from crewai import Crew, Process

from agents.business_analyst import create_business_analyst
from agents.design_agent import create_design_agent
from agents.developer_agent import create_developer
from agents.testing_agent import create_testing_agent

from tasks.user_story_task import create_user_story_task
from tasks.design_task import create_design_task
from tasks.dev_task import create_dev_task
from tasks.testing_task import create_testing_task

from artifacts.artifact_manager import save_artifact
from memory.vector_store import VectorStore

load_dotenv()

# Max characters to pass between agents (keeps within Groq's TPM limits)
MAX_CONTEXT = 3000


def _truncate(text, limit=MAX_CONTEXT):
    """Truncate text to fit within token limits while keeping useful content."""
    if len(text) <= limit:
        return text
    return text[:limit] + "\n\n[... truncated for brevity ...]"


class ProjectLead:
    """Orchestrates the AI development workflow using CrewAI agents."""

    AGENTS = ["Business Analyst", "Design Agent", "Developer Agent", "Testing Agent"]

    def __init__(self):
        # CrewAI uses litellm — pass model as "groq/model-name"
        # GROQ_API_KEY is read from env automatically
        model_name = os.getenv("MODEL_NAME", "llama-3.1-8b-instant")
        self.llm = f"groq/{model_name}"

        self.ba = create_business_analyst(self.llm)
        self.designer = create_design_agent(self.llm)
        self.developer = create_developer(self.llm)
        self.tester = create_testing_agent(self.llm)

        try:
            self.vector_store = VectorStore()
        except Exception:
            self.vector_store = None

    def _run_single(self, agent, task, retries=3):
        """Run a single agent/task pair with retry + backoff for rate limits."""
        for attempt in range(retries):
            try:
                crew = Crew(
                    agents=[agent],
                    tasks=[task],
                    process=Process.sequential,
                    verbose=True,
                )
                result = crew.kickoff()
                return result.raw
            except Exception as e:
                err = str(e).lower()
                if "rate" in err or "limit" in err or "429" in err:
                    wait = 10 * (attempt + 1)
                    print(f"  ⏳ Rate limited. Waiting {wait}s before retry {attempt + 2}/{retries}...")
                    time.sleep(wait)
                else:
                    raise
        raise RuntimeError(f"Agent failed after {retries} retries due to rate limits.")

    def run(self, requirement, on_status=None):
        """
        Run the full development pipeline.

        Args:
            requirement: The business requirement string.
            on_status: Optional callback(agent_name, status) for UI updates.

        Returns:
            dict with keys: user_stories, design, code, tests
        """
        results = {}
        comm_log = []

        def status(agent, state, msg=""):
            if on_status:
                on_status(agent, state)
            log_msg = f"Project Lead → {agent}: {state}"
            if msg:
                log_msg += f" — {msg}"
            comm_log.append(log_msg)
            print(f"  {log_msg}")

        # ── Step 1: Business Analyst ─────────────────────────
        status("Business Analyst", "running", "Generating user stories")
        task = create_user_story_task(self.ba, requirement)
        user_stories = self._run_single(self.ba, task)
        results["user_stories"] = user_stories
        save_artifact("requirements/user_stories.md", user_stories)
        self._store_memory("user_stories", user_stories)
        status("Business Analyst", "completed", "User stories generated")

        # Brief pause to respect rate limits
        time.sleep(5)

        # ── Step 2: Design Agent ─────────────────────────────
        status("Design Agent", "running", "Creating system design")
        task = create_design_task(self.designer, _truncate(user_stories))
        design = self._run_single(self.designer, task)
        results["design"] = design
        save_artifact("design/architecture.md", design)
        self._store_memory("design", design)
        status("Design Agent", "completed", "Design document created")

        time.sleep(5)

        # ── Step 3: Developer Agent ──────────────────────────
        status("Developer Agent", "running", "Generating backend code")
        task = create_dev_task(self.developer, _truncate(user_stories, 1500), _truncate(design, 1500))
        code = self._run_single(self.developer, task)
        results["code"] = code
        save_artifact("code/backend/generated_code.md", code)
        self._store_memory("code", code)
        status("Developer Agent", "completed", "Code generated")

        time.sleep(5)

        # ── Step 4: Testing Agent ────────────────────────────
        status("Testing Agent", "running", "Generating test cases")
        task = create_testing_task(self.tester, _truncate(code))
        tests = self._run_single(self.tester, task)
        results["tests"] = tests
        save_artifact("tests/test_cases.md", tests)
        self._store_memory("tests", tests)
        status("Testing Agent", "completed", "Test cases generated")

        results["comm_log"] = comm_log
        return results

    def _store_memory(self, doc_id, text):
        """Store artifact in ChromaDB vector memory."""
        if self.vector_store:
            try:
                self.vector_store.add(doc_id, text)
            except Exception:
                pass