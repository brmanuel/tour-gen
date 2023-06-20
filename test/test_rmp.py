import pytest

from src.algorithm.rmp import Rmp
from src.model.basic_tour import BasicTour
from src.algorithm.solver import Solver
from stubs.stub_tour import StubTour
from stubs.stub_input import StubInput


def test_rmp_with_candidates():
    tasks = [f"task_{i}" for i in range(10)]
    candidates = [
        StubTour([f"task_{task}" for task in tour])
        for tour in [
                [0,1,2,3],
                [4],
                [5,6,7,8,9],
                [0,1],
                [1,2],
                [2,3],
                [3,4],
                [4,5],
                [5,6],
                [6,7],
                [7,8],
                [8,9]
        ]
    ]
    rmp = Rmp(tasks, candidates)
    rmp.solve()
    solution = rmp.get_solution()
    for i in range(0,3):
        assert solution[candidates[i]] == 1.0
    for i in range(3,10):
        assert solution[candidates[i]] == 0.0

def test_rmp_with_initial_solution():
    source = 10
    target = 11
    edges = set([
        (source,0),(0,1),(1,2),(2,3),(3,target),
        (source,4),(4,target),
        (source,5),(5,6),(6,7),(7,8),(8,9),(9,target),
        (source,0),(0,1),(1,target),
        (source,1),(1,2),(2,target),
        (source,2),(2,3),(3,target),
        (source,5),(5,6),(6,target),
        (source,6),(6,7),(7,target),
        (source,7),(7,8),(8,target),
        (source,8),(8,9),(9,target)
    ])
    input = StubInput(edges, source, target)
    solver = Solver(input, StubTour)
    solver.solve()
    solution = solver.get_solution()
    expected_result = [
        StubTour.create(StubInput.GROUP, [0,1,2,3]),
        StubTour.create(StubInput.GROUP, [4]),
        StubTour.create(StubInput.GROUP, [5,6,7,8,9])
    ]
    for tour in solution:
        assert tour in expected_result
    assert len(expected_result) == len(solution)
    
