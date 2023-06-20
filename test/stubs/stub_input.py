
import networkx as nx
from typing import Set, Tuple

from src.input.input import Input

class StubInput(Input):
    """Adapter to make ordinary digraphs look like an input with a single group GROUP.
    NOTE: the graph must have a topological ordering."""

    GROUP = "GROUP"
    
    def __init__(
        self,
        edges : Set[Tuple["Node"]],
        source : "Node",
        target : "Node"
    ):
        self._graph = nx.DiGraph()
        self._graph.add_edges_from(edges)
        assert nx.is_directed_acyclic_graph(self._graph)
        
        self._edges = edges
        self._source = source
        self._target = target        
        self._tasks = [
            task
            for task in list(nx.topological_sort(self._graph))
            if task not in [source, target]
        ]

    def get_edges_between(self, left_task, right_task):
        edge = (left_task, right_task)
        if edge not in self._edges:
            return set()
        return set([edge])

    def get_source_edges(self, group, task):
        edge = (self._source, task)
        if group != StubInput.GROUP or edge not in self._edges:
            return set()
        return set([edge])
        

    def get_target_edges(self, task, group):
        edge = (task, self._target)
        if group != StubInput.GROUP or edge not in self._edges:
            return set()
        return set([edge])

    def get_tasks_for_group(self, group):
        if group != StubInput.GROUP:
            return set()
        return set(self._tasks)

    def get_tasks(self):
        return set(self._tasks)

    def get_groups(self):
        return set([StubInput.GROUP])

    def get_depot_resources(self, group):
        return tuple([])

    def propagate_resources(self, left_resources, edge):
        return tuple([])
        
    def are_resources_valid_at_task(self, resources, task):
        return True

    def are_resources_valid_at_edge(self, resources, edge):
        return True
    
    def get_start_time_of_task(self, task):
        return self._tasks.index(task)

        
        
