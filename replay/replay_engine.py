"""
Replay / Time-Travel Engine
============================
ExecutionTracker — records agent steps during a pipeline run.
ReplayEngine     — loads and replays past execution logs.
"""

import json
import os
import glob
from datetime import datetime

# Default log directory (relative to project root)
DEFAULT_LOG_DIR = os.path.join(os.path.dirname(__file__), "..", "execution_logs")


class ExecutionTracker:
    """Records each agent step during a pipeline execution."""

    def __init__(self):
        self.started_at = datetime.now().isoformat()
        self.steps = []

    def record_step(self, agent_name, status, input_data="", output_data=""):
        """Append a step entry with an automatic timestamp."""
        self.steps.append({
            "agent_name": agent_name,
            "status": status,
            "input_data": input_data[:300] if input_data else "",
            "output_data": output_data[:300] if output_data else "",
            "timestamp": datetime.now().isoformat(),
        })

    def save(self, log_dir=None):
        """
        Persist the run to a JSON file in *log_dir*.
        Filename auto-increments: run_1.json, run_2.json, …
        Returns the path of the saved file.
        """
        log_dir = log_dir or DEFAULT_LOG_DIR
        os.makedirs(log_dir, exist_ok=True)

        existing = glob.glob(os.path.join(log_dir, "run_*.json"))
        next_id = len(existing) + 1
        run_id = f"run_{next_id}"
        filename = f"{run_id}.json"

        data = {
            "run_id": run_id,
            "started_at": self.started_at,
            "completed_at": datetime.now().isoformat(),
            "steps": self.steps,
        }

        path = os.path.join(log_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

        print(f"  📝 Execution log saved: {path}")
        return path


class ReplayEngine:
    """Loads and replays past execution runs."""

    def __init__(self, log_dir=None):
        self.log_dir = log_dir or DEFAULT_LOG_DIR

    def list_runs(self):
        """Return sorted list of run_*.json filenames (newest first)."""
        if not os.path.isdir(self.log_dir):
            return []
        files = [
            f for f in os.listdir(self.log_dir)
            if f.startswith("run_") and f.endswith(".json")
        ]
        files.sort(key=lambda f: self._run_number(f), reverse=True)
        return files

    def load_run(self, filename):
        """Parse and return a run JSON file as a dict."""
        path = os.path.join(self.log_dir, filename)
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @staticmethod
    def replay_steps(run_data):
        """Generator that yields steps one at a time for sequential display."""
        for step in run_data.get("steps", []):
            yield step

    @staticmethod
    def _run_number(filename):
        """Extract the numeric part from run_N.json for sorting."""
        try:
            return int(filename.replace("run_", "").replace(".json", ""))
        except ValueError:
            return 0
