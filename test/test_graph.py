
import pytest
from dataclasses import dataclass
from typing import Any

from src.algorithm.graph import Graph

@dataclass(frozen=True)
class Node:
    id : int
    data : Any

    def __hash__(self):
        return self.id


NODES = [
    Node(0, {"a": 1, "b": "hello"}),
    Node(1, {"a": 2, "b": "there"}),
    Node(2, {"a": 3, "b": "column"}),
    Node(3, {"a": 4, "b": "generation"}),
    Node(4, {"a": 5, "b": "algorithm"}),
]

def test_add_remove_and_get_node():
    graph = Graph()
    for node in NODES:
        graph.add_node(node)
    nodes = graph.get_nodes()
    for node in NODES:
        assert node in nodes
    for node in NODES:
        graph.remove_node(node)
    nodes = graph.get_nodes()
    assert len(nodes) == 0
        
def test_add_neighbors():
    graph = Graph()
    for node in NODES:
        graph.add_node(node)
    graph.add_edge(NODES[0], NODES[1])
    graph.add_edge(NODES[0], NODES[2])
    graph.add_edge(NODES[0], NODES[3])
    graph.add_edge(NODES[1], NODES[4])
    graph.add_edge(NODES[2], NODES[4])
    graph.add_edge(NODES[3], NODES[4])

    out_neighbors = graph.get_out_neighbors(NODES[0])
    in_neighbors = graph.get_in_neighbors(NODES[4])
    for node in [NODES[1], NODES[2], NODES[3]]:
        assert node in out_neighbors
        assert node in in_neighbors

    graph.remove_edge(NODES[0], NODES[1])
    graph.remove_edge(NODES[0], NODES[2])
    graph.remove_edge(NODES[0], NODES[3])
    assert len(graph.get_out_neighbors(NODES[0])) == 0

def test_node_cost_and_shortest_path():
    graph = Graph()
    for node in NODES:
        graph.add_node(node)
    graph.add_edge(NODES[0], NODES[1])
    graph.add_edge(NODES[0], NODES[2])
    graph.add_edge(NODES[0], NODES[3])
    graph.add_edge(NODES[1], NODES[4])
    graph.add_edge(NODES[2], NODES[4])
    graph.add_edge(NODES[3], NODES[4])

    graph.set_node_cost(NODES[1], 2.5)
    graph.set_node_cost(NODES[2], 3.5)
    graph.set_node_cost(NODES[3], 4.5)
    path, cost = graph.get_shortest_s_t_path_with_weight(NODES[0], NODES[4])
    assert cost == 2.5
    assert path == [NODES[0], NODES[1], NODES[4]]

    graph.set_node_cost(NODES[1], 6.5)
    graph.set_node_cost(NODES[2], 5.5)
    path, cost = graph.get_shortest_s_t_path_with_weight(NODES[0], NODES[4])
    assert cost == 4.5
    assert path == [NODES[0], NODES[3], NODES[4]]
    


    
