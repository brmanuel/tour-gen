from typing import Set
from pyscipopt import Model, quicksum
from pprint import pprint

from src.algorithm.prizing import Prizing
from src.algorithm.prizing_callback import PrizingCallback
from src.input.input import Input
from src.model.tour_factory import TourFactory
from src.model.tour import Tour

class CallbackSolver:
    """Class setting up SCIP solver using a prizing callback to do
    column generation internally."""
    def __init__(self, input : Input, tour_factory : TourFactory):
        self._solution = None
        self._input = input
        self._tour_factory = tour_factory


    def get_solution(self):
        assert self._solution is not None
        return self._solution

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
        candidates = self._find_initial_solution(self._input, self._tour_factory)
        prizing = Prizing(self._input, self._tour_factory)
        prizer = PrizingCallback()

        model = Model("Tour Generation (with prizing callback)")
        model.setPresolve(0)
        model.includePricer(prizer, "PrizingCallback", "Shortest path in resource expanded graph.")


        selection_variables = {}
        cover_constraints = {}
        task_to_tours = {}
        for idx, tour in enumerate(candidates):
            selection_variables[tour] = model.addVar(
                name=f"cand_{idx}",
                vtype="B",
                obj=1.0
            )
            for task in tour.get_tasks():
                if task not in task_to_tours:
                    task_to_tours[task] = set()
                task_to_tours[task].add(tour)
                
        for task, tours in task_to_tours.items():
            cover_task_cons = model.addCons(
                quicksum(selection_variables[tour] for tour in tours) == 1,
                f"cover_{task}",
                separate=False,
                modifiable=True
            )
            cover_constraints[task] = cover_task_cons
        
        prizer.data = {}
        prizer.data["tour_to_var"] = selection_variables
        prizer.data["task_to_constr"] = cover_constraints
        prizer.data["prizing"] = prizing
        

        model.setMinimize()
        model.optimize()

        sol = model.getBestSol()
        self._solution = set()
        objective = 0
        task_coverage = { task : 0 for task in self._input.get_tasks() }
        for tour, var in prizer.data["tour_to_var"].items():
            value = sol[var]
            objective += value
            if value > 0.5:
                self._solution.add(tour)
            for task in tour.get_tasks():
                task_coverage[task] += value
        #pprint(task_coverage)
        print("Objective value: ", objective)
        assert all(abs(cov - 1) < 1e-5 for cov in task_coverage.values())
        
        
