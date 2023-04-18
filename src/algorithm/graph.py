"""Wrapper around Networkx Digraph."""

import networkx

class Graph:
    def __init__(self):
        self._graph = networkx.DiGraph()

    def add_node(self, node):
        self._graph.add_node(node)

    def add_edge(self, source, target):
        self._graph.add_edge(source, target)

    def get_shortest_s_t_path_with_weight(self, source, target):
        """Returns a shortest s-t-path and the weight of this path."""
        pred_map, dist_map = networkx.dijkstra_predecessor_and_distance(
            self._graph, source, weight="weight")
        path = []
        current = target
        while current != source:
            path = [current] + path
            assert current in pred_map, "No source-target path exists!"
            current = pred_map[current]
        path = [source] + path
        return path, dist_map[target]
        

    def set_node_cost(self, node, cost):
        for _,_,data in self._graph.in_edges(node, data=True):
            data["weight"] = cost