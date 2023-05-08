from dataclasses import dataclass
from typing import Any

from src.model.tour import Tour
from src.input.input import Input 
from src.algorithm.graph import Graph

@dataclass
class Node:
    id : int
    type : str 
    data : Any
    resources : Any

    def __hash__(self):
        return self.id


class Prizing:

    def __init__(self, input : Input):
        self._num_nodes = 0
        self._graph = self._build_graph(input)

    def _create_node(self, type, data, resources):
        self._num_nodes += 1
        return Node(self._num_nodes, type, data, resources)

    def _create_neighbor(input, left_resources, edge, right_task):
        right_resources = input.propagate_resources(
            left_resources, edge
        )
        if input.are_resources_valid_at_task(right_resources, right_task):
            return self._create_node("task", right_task, right_resources)
        return None

    
    def _build_graph(self, input : Input):
        graph = Graph()
        source_node = self._create_node("source", None, None)
        target_node = self._create_node("target", None, None)
        graph.add_node(source_node)
        graph.add_node(target_node)
        groups = input.get_groups()
        for group in groups:
            group_tasks = input.get_tasks_for_group(group)
            group_tasks = sorted(group_tasks, key=lambda task: Input.get_start_time_of_task(task))
            depot_start = self._create_node("depot_start", group, input.get_depot_resources(group))
            depot_end = self._create_node("depot_end", group, None)
            graph.add_node(depot_start)
            graph.add_node(depot_end)
            graph.add_edge(source_node, depot_start)
            graph.add_edge(depot_end, target_node)

            task_to_nodes = {i: set() for i in range(len(group_tasks))}
            
            for i in range(len(group_tasks)):
                from_task = group_tasks[i]
                edges = get_source_edges(group, from_task)

                for edge in edges:
                    from_node = _create_neighbor(
                        input,
                        input.get_depot_resources(group),
                        edge,
                        from_task
                    )
                    if from_node is not None:
                        graph.add_node(from_node)
                        graph.add_edge(depot_node, from_node)
                        task_to_nodes[i].add(from_node)
                                   
                
                for j in range(i+1, len(group_tasks)):
                    to_task = group_tasks[j]
                    edges = get_edges_between(from_task, to_task)
                    for edge in edges:
                        for left_node in task_to_nodes[i]:
                            right_node = _create_neighbor(
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

        graph = _clean_graph(graph, source_node, target_node)
                        
        return graph

    def _clean_graph(graph : Graph, source, target):
        dead_ends = set()
        for node in graph.get_nodes():
            if len(node.get_out_neighbors()) == 0:
                dead_ends.add(node)
        for to_node in dead_ends:
            for from_node in graph.get_in_neighbors(to_node):
                graph.remove_edge(from_node, to_node)
                if len(graph.get_out_neighbors(from_node)) == 0:
                    dead_ends.add(from_node)
            graph.remove_node(to_node)
        return graph


    def compute_prizing(duals):
        pass

    def get_best_candidate_cost(self) -> float:
        pass

    def get_best_candidate() -> Tour:
        pass


