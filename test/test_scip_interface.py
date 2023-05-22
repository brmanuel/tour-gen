
from pyscipopt import Model, SCIP_PARAMSETTING
import pytest


def test_primals():
    model = Model()
    # explicitly set lower bound. default is 0
    x = model.addVar("x", lb=None)
    y = model.addVar("y", vtype="INTEGER", lb=None)
    model.setObjective(x + y)
    model.addCons(x >= -1)
    model.addCons(y >= -2.5)
    model.optimize()
    sol = model.getBestSol()
    assert sol[x] == -1
    assert sol[y] == -2

def test_duals():
    primal = Model()
    x = primal.addVar("x", lb=0)
    y = primal.addVar("y", lb=0)
    c1 = primal.addCons(x + 2*y <= 21)
    c2 = primal.addCons(2*x + y <= 24)
    primal.setObjective(x+y, sense="maximize")
    # to get duals, we need to switch off some features of SCIP!
    # c.f. https://github.com/scipopt/PySCIPOpt/issues/136
    primal.setPresolve(SCIP_PARAMSETTING.OFF)
    primal.setHeuristics(SCIP_PARAMSETTING.OFF)
    primal.disablePropagation()
    primal.optimize()

    dual = Model()
    a = dual.addVar("a", lb=0)
    b = dual.addVar("b", lb=0)
    d1 = dual.addCons(a + 2*b >= 1)
    d2 = dual.addCons(2*a + b >= 1)
    dual.setObjective(21*a + 24*b, sense="minimize")
    dual.setPresolve(SCIP_PARAMSETTING.OFF)
    dual.setHeuristics(SCIP_PARAMSETTING.OFF)
    dual.disablePropagation()
    dual.optimize()

    primal_sol = primal.getBestSol()
    dual_sol = dual.getBestSol()
    print("primal")
    print(primal_sol[x], primal_sol[y])
    print(primal.getDualsolLinear(c1), primal.getDualsolLinear(c2))
    print("dual")
    print(dual_sol[a], dual_sol[b])
    print(dual.getDualsolLinear(d1), dual.getDualsolLinear(d2))
    
    assert primal_sol[x] == 9
    assert primal_sol[y] == 6
    assert primal.getDualsolLinear(c2) == dual_sol[b]
    assert primal.getDualsolLinear(c1) == dual_sol[a]

def test_duals_2():
    primal = Model()
    x1 = primal.addVar("x1", lb=0, ub=None)
    x2 = primal.addVar("x2", lb=None, ub=0)
    x3 = primal.addVar("x3", lb=None, ub=None)
    c1 = primal.addCons(2*x1 - 7*x2 + 5*x3 == -2)
    c2 = primal.addCons(x2 <= 3)
    c3 = primal.addCons(x1 - 7*x3 >= 8)
    c4 = primal.addCons(5*x1 - x2 >= 0)
    primal.setObjective(4*x1 + 3*x2 - 2*x3, sense="minimize")
    # to get duals, we need to switch off some features of SCIP!
    # c.f. https://github.com/scipopt/PySCIPOpt/issues/136
    primal.setPresolve(SCIP_PARAMSETTING.OFF)
    primal.setHeuristics(SCIP_PARAMSETTING.OFF)
    primal.disablePropagation()
    primal.optimize()
    
    primal_sol = primal.getBestSol()
    del primal

    dual = Model()
    y1 = dual.addVar("y1", lb=None, ub=None)
    y2 = dual.addVar("y2", lb=None, ub=0)
    y3 = dual.addVar("y3", lb=0, ub=None)
    y4 = dual.addVar("y4", lb=0, ub=None)
    d1 = dual.addCons(2*y1 + y3 + 5*y4 <= 4)
    d2 = dual.addCons(-7*y1 + y2 - y4 >= 3)
    d3 = dual.addCons(5*y1 - 7*y3 == -2)
    dual.setObjective(-2*y1 + 3*y2 + 8*y3, sense="maximize")

    dual.setPresolve(SCIP_PARAMSETTING.OFF)
    dual.setHeuristics(SCIP_PARAMSETTING.OFF)
    dual.disablePropagation()
    dual.optimize()

    dual_sol = dual.getBestSol()
    # assert primal_sol[x1] == dual.getDualsolLinear(d1)
    # assert primal_sol[x2] == dual.getDualsolLinear(d2)
    # assert primal_sol[x3] == dual.getDualsolLinear(d3)
    # assert primal.getDualsolLinear(c1) == dual_sol[y1]
    # assert primal.getDualsolLinear(c2) == dual_sol[y2]
    # assert primal.getDualsolLinear(c3) == dual_sol[y3]
    # assert primal.getDualsolLinear(c4) == dual_sol[y4]
    
