from pyscipopt import Pricer, SCIP_RESULT
from src.algorithm.prizing import Prizing

class PrizingCallback(Pricer):

    def pricerredcost(self):
        # Retrieving the dual solutions
        duals = {}
        for task, constr in self.data["task_to_constr"].items():
            duals[task] = self.model.getDualsolLinear(constr)

        # Solve prizing
        self.data["prizing"].compute_prizing(duals)
        best_cost = self.data["prizing"].get_best_candidate_cost()

        if best_cost < -1e-08:
            # Add the improving variable to the problem
            candidate = self.data["prizing"].get_best_candidate()
            idx = len(self.data["tour_to_var"])
            newVar = self.model.addVar(
                name=f"cand_{idx}",
                vtype="B",
                obj=1.0,
                pricedVar=True
            )
            for task in candidate.get_tasks():
                constr = self.data["task_to_constr"][task]
                self.model.addConsCoeff(constr, newVar, 1.0)

            self.data["tour_to_var"][candidate] = newVar

        return {"result": SCIP_RESULT.SUCCESS}

    def pricerinit(self):
        # Store the transformed constraints instead of the original ones
        # This is necessary to access their duals-values
        for task, constr in self.data["task_to_constr"].items():
            self.data["task_to_constr"][task] = self.model.getTransformedCons(constr)
        print("done pricerinit")
