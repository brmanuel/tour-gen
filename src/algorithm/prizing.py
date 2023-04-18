from src.model.tour import Tour
from src.input.input import Input 
from src.algorithm.graph import Graph

class Prizing:

    def __init__(self, input : Input):
        self._source = {"id": "SOURCE"}
        self._target = {"id": "TARGET"}
        self._graph = Prizing._build_graph(input, self._source, self._target)

    @staticmethod
    def _build_graph(input : Input, source, target):
        graph = Graph()
        graph.add_node(source)
        graph.add_node(target)
        groups = input.get_groups()
        for group in groups:
            group_tasks = input.get_tasks_for_group(group)
            group_tasks = sorted(group_tasks, key=lambda task: Input.get_start_time_of_task(task))
            for i in range(len(group_tasks)):
                for j in range(i+1, len(group_tasks)):
                    pass
        return None


    def compute_prizing(duals):
        pass

    def get_best_candidate_cost(self) -> float:
        pass

    def get_best_candidate() -> Tour:
        pass


