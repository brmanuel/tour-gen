import json

from src.input.nvidia_input import NvidiaInput

class StubNvidiaInput(NvidiaInput):
    """Mock input class where all states are valid to ease testing."""
    @staticmethod
    def from_file(filename):
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return StubNvidiaInput(data)

    
    def are_resources_valid_at_task(self, resources, task_id):
        return True

    def are_resources_valid_at_edge(self, resources, edge_id):
        return True



