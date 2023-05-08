import pytest
from src.algorithm.prizing import Prizing
from src.input.nvidia_input import NvidiaInput


@pytest.fixture
def load_input():
    def _load_input(path):
        return NvidiaInput.from_file(path)
    return _load_input


def test_small_input(load_input):
    input = load_input("input_data/small_graph.json")
    prizing = Prizing(input)
    print(prizing._graph)