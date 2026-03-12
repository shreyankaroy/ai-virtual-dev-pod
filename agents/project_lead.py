from utils.logger import log
from utils.artifact_manager import save_artifact
from execution.code_generator import generate_code_files
from execution.devops_generator import generate_devops_files
from execution.test_runner import run_tests as execute_tests
from execution.debug_generator import apply_debug_fixes
from execution.test_generator import generate_test_files
from utils.memory_manager import update_memory
from memory.memory_retriever import retrieve_memory


class ProjectLeadAgent:
    """
    The Project Lead orchestrates the AI development workflow
    using a shared project_state.
    """

    def __init__(
        self,
        business_analyst,
        system_designer,
        developer,
        tester,
        devops,
        debugger
    ):
        self.business_analyst = business_analyst
        self.system_designer = system_designer
        self.developer = developer
        self.tester = tester
        self.devops = devops
        self.debugger = debugger

    # ---------------------------------------------------
    # BUSINESS ANALYST
    # ---------------------------------------------------

    def run_business_analyst(self, state):

        if state.get("memory_context") is None:

            memory_context = retrieve_memory(state["idea"])
            state["memory_context"] = memory_context

            log.info(f"Memory context loaded: {memory_context}")

        log.info("Project Lead: Requesting user stories")

        user_stories = self.business_analyst.generate_user_stories(
            state["idea"],
            state["memory_context"]
        )

        state["user_stories"] = user_stories

        save_artifact("user_stories.json", user_stories)

        update_memory("user_stories", user_stories)

    # ---------------------------------------------------
    # SYSTEM DESIGN
    # ---------------------------------------------------

    def run_system_designer(self, state):

        log.info("Project Lead: Requesting system design")

        system_design = self.system_designer.design_system(
            state["user_stories"]["stories"],
            state.get("memory_context")
        )

        state["system_design"] = system_design

        save_artifact("architecture.json", system_design)

        update_memory("system_design", system_design)

    # ---------------------------------------------------
    # DEVELOPER
    # ---------------------------------------------------

    def run_developer(self, state):

        log.info("Project Lead: Requesting code generation")

        code_plan = self.developer.generate_code(
            state["system_design"],
            state.get("memory_context")
        )

        state["code_plan"] = code_plan

        save_artifact("code_plan.json", code_plan)

        generate_code_files(code_plan)

        update_memory("code_plan", code_plan)

    # ---------------------------------------------------
    # TESTER
    # ---------------------------------------------------

    def run_tester(self, state):

        log.info("Project Lead: Requesting test cases")

        tests = self.tester.generate_tests(
            state["system_design"],      # ← add this back
            state["code_plan"]
        )

        state["tests"] = tests
        save_artifact("test_plan.json", tests)
        generate_test_files(tests)
        update_memory("tests", tests)

        passed, test_output = execute_tests()
        state["test_output"] = test_output

        if passed:
            state["test_results"] = "pass"
            log.success("All tests passed")
        else:
            state["test_results"] = "fail"
            log.warning("Tests failed")

    # ---------------------------------------------------
    # DEBUGGER
    # ---------------------------------------------------

    def run_debugger(self, state):

        MAX_DEBUG_ATTEMPTS = 3

        for attempt in range(1, MAX_DEBUG_ATTEMPTS + 1):

            log.warning(
                f"Project Lead: Debugging code (attempt {attempt}/{MAX_DEBUG_ATTEMPTS})"
            )

            failing_tests = state.get("test_output", "Tests failed")

            fixes = self.debugger.fix_code(
                state["code_plan"]["files"],
                failing_tests
            )

            apply_debug_fixes(fixes)

            state.setdefault("code_plan", {})
            state["code_plan"]["debug_fixes"] = fixes

            passed, test_output = execute_tests()

            state["test_output"] = test_output

            if passed:

                state["test_results"] = "pass"

                log.success("Debug successful — all tests passed")

                return

            log.warning(f"Debug attempt {attempt} failed")

        log.error("Max debug attempts reached — moving on")

        state["test_results"] = "fail"

    # ---------------------------------------------------
    # DEVOPS
    # ---------------------------------------------------

    def run_devops(self, state):

        log.info("Project Lead: Generating deployment configuration")

        devops_files = self.devops.generate_devops(
            state["code_plan"]["files"],
            state["tests"]
        )

        state["devops"] = devops_files

        save_artifact("devops_plan.json", devops_files)

        generate_devops_files(devops_files)

        update_memory("devops", devops_files)

        log.success("DevOps configuration generated")