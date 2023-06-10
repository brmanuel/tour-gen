import pytest
from typing import Set, List

from src.model.tour import Tour
from src.algorithm.rmp import Rmp

class TestTour(Tour):
    def __init__(self, tasks : List["Task"]):
        self._tasks = tuple(tasks)
        
    def get_tasks(self):
        return self._tasks

def test_rmp():
    tasks = [f"task_{i}" for i in range(10)]
    candidates = [
        TestTour([f"task_{i}" for i in tasks])
        for tasks in [
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
    for i in range(0,4):
        assert solution[candidates[i]] == 1.0
    for i in range(4,10):
        assert solution[candidates[i]] == 0.0
