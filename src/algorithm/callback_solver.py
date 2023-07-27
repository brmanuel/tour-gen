
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
        prizer = PrizingCallback(prizing)

        model = Model("Tour Generation (with prizing callback)")
        model.includePricer(prizer, "PrizingCallback")

        selection_variables = {}
        cover_constraints = {}
        task_to_tours = {}
        for idx, tour in enumerate(candidates):
            selection_variables[tour] = model.addVar(
                name=f"cand_{idx}",
                vtype="B"
                obj=1.0
            )
            for task in tour.get_tasks():
                if task not in task_to_tours:
                    task_to_tours[task] = set()
                task_to_tours[task].add(tour)
                
        for task, tours in task_to_tours.items():
            cover_task_cons = model.addCons(
                quicksum(selection_variables[tour] for tour in tours) == 1, f"cover_{task}"
            )
            cover_constraints[task] = cover_task_cons
        
        prizer.data = {}
        prizer.data["tour_to_var"] = selection_variables
        prizer.data["task_to_constr"] = cover_constraints

        model.setMinimize()
        model.optimize()

        sol = model.getBestSol()
        primal_solution = {}
        for tour, var in prizer.data["tour_to_var"].items():
            primal_solution[tour] = sol[var]

        self._solution = primal_solution
        
        