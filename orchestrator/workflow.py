from agents.project_lead import ProjectLeadAgent
from agents.business_analyst import BusinessAnalystAgent
from agents.system_designer import SystemDesignerAgent
from agents.developer_agent import DeveloperAgent
from agents.testing_agent import TestingAgent
from agents.devops_agent import DevOpsAgent
from agents.debug_agent import DebugAgent
from orchestrator.router import decide_next_agent
from utils.metrics import MetricsCollector


class DevelopmentWorkflow:

    def __init__(self):

        self.business_analyst = BusinessAnalystAgent()
        self.system_designer = SystemDesignerAgent()
        self.developer = DeveloperAgent()
        self.tester = TestingAgent()
        self.devops = DevOpsAgent()
        self.debugger = DebugAgent()

        self.project_lead = ProjectLeadAgent(
            business_analyst=self.business_analyst,
            system_designer=self.system_designer,
            developer=self.developer,
            tester=self.tester,
            devops=self.devops,
            debugger=self.debugger
        )

    def run(self, product_idea):

        project_state = {
            "idea": product_idea,
            "user_stories": None,
            "system_design": None,
            "code_plan": None,
            "tests": None,
            "devops": None,
            "test_results": None,
            "metrics": {}
        }

        metrics = MetricsCollector()
        project_state["metrics_collector"] = metrics

        while True:

            print("\nSTATE:", project_state)

            next_agent = decide_next_agent(project_state)

            print("NEXT AGENT:", next_agent)

            if next_agent == "complete":
                break

            if next_agent == "business_analyst":
                metrics.start("business_analyst")
                self.project_lead.run_business_analyst(project_state)
                metrics.end("business_analyst")

            elif next_agent == "system_designer":
                metrics.start("system_designer")
                self.project_lead.run_system_designer(project_state)
                metrics.end("system_designer")

            elif next_agent == "developer":
                metrics.start("developer")
                self.project_lead.run_developer(project_state)
                metrics.end("developer")

            elif next_agent == "tester":
                metrics.start("tester")
                self.project_lead.run_tester(project_state)
                metrics.end("tester")


            elif next_agent == "debugger":
                metrics.start("debugger")
                self.project_lead.run_debugger(project_state)
                metrics.end("debugger")

            elif next_agent == "devops":
                metrics.start("devops")
                self.project_lead.run_devops(project_state)
                metrics.end("devops")


        project_state["metrics"] = metrics.report()

        return project_state