from dataclasses import dataclass
from typing import Any, Dict

from src.model.tour import Tour
from src.input.input import Input 
from src.algorithm.graph import Graph

@dataclass(frozen=True)
class Node:
    type : str 
    data : Any
    resources : Any

class Prizing:

    def __init__(self, input : Input, tour_factory):
        self._input = input
        self._graph, self._source_node, self._target_node = Prizing.build_graph(input)
        self._tour_factory = tour_factory

    @staticmethod
    def build_graph(input : Input):
        nodes = {}
        def create_node(type, data, resources):
            if (type, data, resources) not in nodes:
                nodes[(type, data, resources)] = Node(type, data, resources)
            return nodes[(type, data, resources)]

        def create_neighbor(input, left_resources, edge, right_task):
            right_resources = input.propagate_resources(
                left_resources, edge
            )
            if input.are_resources_valid_at_task(right_resources, right_task):
                return create_node("task", right_task, right_resources)
            return None

        graph = Graph()        
        source_node = create_node("source", None, None)
        target_node = create_node("target", None, None)
        graph.add_node(source_node)
        graph.add_node(target_node)
        groups = input.get_groups()
        for group in groups:
            group_tasks = input.get_tasks_for_group(group)
            group_tasks = sorted(group_tasks, key=lambda task: input.get_start_time_of_task(task))
            depot_start = create_node("depot_start", group, input.get_depot_resources(group))
            depot_end = create_node("depot_end", group, None)
            graph.add_node(depot_start)
            graph.add_node(depot_end)
            graph.add_edge(source_node, depot_start)
            graph.add_edge(depot_end, target_node)

            task_to_nodes = {i: set() for i in range(len(group_tasks))}
            
            for i in range(len(group_tasks)):
                from_task = group_tasks[i]
                edges = input.get_source_edges(group, from_task)

                for edge in edges:
                    from_node = create_neighbor(
                        input,
                        input.get_depot_resources(group),
                        edge,
                        from_task
                    )
                    if from_node is not None:
                        graph.add_node(from_node)
                        graph.add_edge(depot_start, from_node)
                        task_to_nodes[i].add(from_node)
                                   
                
                for j in range(i+1, len(group_tasks)):
                    to_task = group_tasks[j]
                    edges = input.get_edges_between(from_task, to_task)
                    for edge in edges:
                        for left_node in task_to_nodes[i]:
                            right_node = create_neighbor(
                                input,
                                left_node.resources,
                                edge,
                                to_task
                            )
                            if right_node is not None:
                                graph.add_node(right_node)
                                graph.add_edge(left_node, right_node)
                                task_to_nodes[j].add(right_node)

                edges = input.get_target_edges(from_task, group)
                for node in task_to_nodes[i]:
                    for edge in edges:
                        final_resources = input.propagate_resources(
                            node.resources, 
                            edge
                        )
                        if input.are_resources_valid_at_edge(final_resources, edge):
                            graph.add_edge(node, depot_end)

        graph = Prizing._clean_graph(graph, source_node, target_node)
        return graph, source_node, target_node

    @staticmethod
    def _clean_graph(graph : Graph, source, target):
        dead_ends = set()
        for node in graph.get_nodes():
            if node in [source, target]:
                continue
            if len(graph.get_out_neighbors(node)) == 0:
                dead_ends.add(node)
        while len(dead_ends) > 0:
            to_node = dead_ends.pop()
            predecessors = graph.get_in_neighbors(to_node)
            for from_node in predecessors:
                graph.remove_edge(from_node, to_node)
                if len(graph.get_out_neighbors(from_node)) == 0:
                    dead_ends.add(from_node)
            graph.remove_node(to_node)
        return graph


    def compute_prizing(self, duals : Dict["Task", float]):
        """Set the costs of all nodes in the graph accoring to duals,
        then compute the shortest tour."""
        for node in self._graph.get_nodes():
            if node.type == "task":
                task = node.data
                self._graph.set_node_cost(node, -duals[task])
        # reduced_cost(s) = 1 - sum_{task on s} dual_val(task)
        path, weight = self._graph.get_shortest_s_t_path_with_weight(
            self._source_node, self._target_node
        )
        weight += 1
        assert path[0].type == "source"
        assert path[1].type == "depot_start"
        assert path[-2].type == "depot_end"
        assert path[-1].type == "target"
        group = path[1].data
        tasks = [path[i].data for i in range(2,len(path)-2)]
        self._best_candidate = self._tour_factory.create(group, tasks)
        self._best_candidate_cost = weight
        

    def get_best_candidate_cost(self) -> float:
        assert self._best_candidate_cost is not None
        return self._best_candidate_cost

    def get_best_candidate(self) -> Tour:
        assert self._best_candidate is not None
        return self._best_candidate


