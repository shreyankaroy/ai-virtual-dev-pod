import time


class MetricsCollector:

    def __init__(self):
        self._start_times = {}
        self.metrics = {}

    def start(self, agent_name):
        self._start_times[agent_name] = time.time()

    def end(self, agent_name):
        if agent_name in self._start_times:
            duration = time.time() - self._start_times[agent_name]
            self.metrics[agent_name] = round(duration, 2)

    def report(self):
        return self.metrics