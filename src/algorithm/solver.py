


class Solver:

    def __init__(self, input : Input, tour_factory):
        self._solution = None
        self._input = input
        self._tour_factory = tour_factory

    @staticmethod
    def _find_initial_solution(input : Input) -> Set[Tour]:
        """Generate the trivial solution where every task is on a
        separate tour."""
        handled_tasks = set()
        solution = set()
        for group in input.get_groups():
            for task in input.get_tasks_for_group(group):
                if task not in handled_tasks:
                    handled_tasks.add(task)
                    solution.add(self._tour_factory.create(group, [task]))
        return solution        
    
    def solve(self):
        """Main column generation loop."""
        candidates = self._find_initial_solution()
        prizing = Prizing(self._input)
        while True:
            rmp = Rmp(self._input, candidates)
            rmp.solve()
            duals = rmp.get_duals()
            prizing.compute_prizing(duals)
            if (prizing.get_best_candidate_cost >= 0):
                break
            candidates.add(prizing.get_best_candidate())
        self._solution = rmp.get_solution()

    def get_solution(self):
        assert self._solution is not None
        return self._solution
    
