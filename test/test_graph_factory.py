import pytest
from src.algorithm.prizing import Prizing
from test.nvidia_input_mock import NvidiaInputMock


@pytest.fixture
def load_input():
    def _load_input(path):
        return NvidiaInputMock.from_file(path)
    return _load_input


def test_small_input(load_input):

    input = load_input("input_data/small_graph.json")
    graph = Prizing.build_graph(input)
    type_map = {
        ("task", "task"): input.get_edges_between,
        ("depot_start", "task"): input.get_source_edges,
        ("task", "depot_end"): input.get_target_edges
    }
    node_map = {}
    for n in graph.get_nodes():
        n_key = (n.type, n.data)
        if n_key not in node_map:
            node_map[n_key] = set()
        node_map[n_key].add(n)

    for depot in input.get_groups():
        # all depots are represented by a node
        assert ("depot_start", depot) in node_map
        assert ("depot_end", depot) in node_map
        
    for src in graph.get_nodes():
        # for every node src, all its outgoing edges are represented in graph as a node
        if src.type in ["source", "target"]:
            continue
        
        for dst_type, dst_id in node_map.keys():
            if dst_type in ["source", "target", "depot_end"]:
                continue
            get_edges = type_map.get((src.type, dst_type), lambda x,y: [])
            edges = get_edges(src.data, dst_id)
            dst_resource_tuples = set(
                tuple(node.resources.values())
                for node in node_map[(dst_type, dst_id)]
            )
            print(f"checking {src} ({dst_type}, {dst_id}) with {len(edges)} edges")
            for edge in edges:
                resources = input.propagate_resources(src.resources, edge)
                assert tuple(resources.values()) in dst_resource_tuples

