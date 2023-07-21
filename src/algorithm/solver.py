
from typing import Set
from pprint import pprint

from src.algorithm.prizing import Prizing
from src.algorithm.rmp import Rmp
from src.input.input import Input
from src.model.tour_factory import TourFactory
from src.model.tour import Tour

class Solver:

    def __init__(self, input : Input, tour_factory : TourFactory):
        self._solution = None
        self._input = input
        self._tour_factory = tour_factory

    @staticmethod
    def _find_initial_solution(input : Input, tour_factory : TourFactory) -> Set[Tour]:
        """Generate the trivial solution where every task is on a
        separate tour."""
        handled_tasks = set()
        solution = set()
        for group in input.get_groups():
            for task in input.get_tasks_for_group(group):
                if task not in handled_tasks:
                    handled_tasks.add(task)
                    solution.add(tour_factory.create(group, [task]))
        return solution        
    
    def solve(self):
        """Main column generation loop."""
        candidates = self._find_initial_solution(self._input, self._tour_factory)
        prizing = Prizing(self._input, self._tour_factory)
        while True:
            rmp = Rmp(self._input.get_tasks(), candidates)
            rmp.solve()
            duals = rmp.get_duals()
            prizing.compute_prizing(duals)
            if (prizing.get_best_candidate_cost() >= 0):
                break
            candidate = prizing.get_best_candidate()
            candidates.add(candidate)
        solution = rmp.get_solution()
        self._solution = set()
        task_coverage = { task : 0 for task in self._input.get_tasks() }
        objective = 0
        for tour, decision_var in solution.items():
            objective += decision_var
            if decision_var > 0.5:
                self._solution.add(tour)
            for task in tour.get_tasks():
                task_coverage[task] += decision_var
        #pprint(task_coverage)
        print("Objective value: ", objective)
        assert all(abs(cov - 1) < 1e-5 for cov in task_coverage.values())

    def get_solution(self):
        assert self._solution is not None
        return self._solution
    
