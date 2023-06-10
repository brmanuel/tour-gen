from pyscipopt import Model, SCIP_PARAMSETTING
from typing import Set

from src.model.tour import Tour

class Rmp:
    def __init__(self, tasks : Set["Task"], candidates : Set[Tour]):
        self._candidates = candidates
        self._tasks = tasks
        self._primal_solution = None
        self._dual_solution = None

    def solve(self):
        self._primal_sol, self._dual_sol = Rmp.solve_rmp(
            self._tasks, self._candidates
        )
        
        
    @staticmethod
    def solve_rmp(tasks : Set["Task"], candidates : Set[Tour]):
        """Creates the RMP LP model, solves it and extracts primal and
        dual solutions."""
        model = Model()

        selection_variables = {}
        cover_constrains = {}
        task_to_tours = {}
        for idx, tour in enumerate(candidates):
            selection_variables[tour] = model.addVar(
                name=f"cand_{idx}",
                vtype="continuous",
                lb=0.0,
                ub=1.0,
                obj=1.0
            )
            for task in tour.get_tasks():
                if task not in task_to_tours:
                    task_to_tours[task] = set()
                task_to_tours[task].add(tour)
                
        for task, tours in task_to_tours.items():
            cover_task_cons = model.addCons()
            for tour in tours:
                model.addConsCoeff(
                    cover_task_cons,
                    selection_variables[tour],
                    1.0
                )
            cover_constraints[task] = cover_task_cons
            
        model.setMinimize()
        
        model.setPresolve(SCIP_PARAMSETTING.OFF)
        model.setHeuristics(SCIP_PARAMSETTING.OFF)
        model.disablePropagation()
        model.optimize()

        sol = model.getBestSol()
        primal_solution = {}
        dual_solution = {}
        for tour in candidates:
            primal_solution[tour] = sol[selection_variables[tour]]

        for task in tasks:
            dual_solution[task] = model.getDualSolVal(cover_constraints[task])

        return primal_solution, dual_solution
    

    def get_duals(self):
        """Returns a mapping from task to its dual solution value."""
        assert self._dual_solution is not None
        return self._dual_solution

    def get_solution(self):
        """Returns a mapping from tour to its coefficient in the solution."""
        assert self._primal_solution is not None
        return self._primal_solution
