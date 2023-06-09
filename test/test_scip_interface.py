
from pyscipopt import Model, SCIP_PARAMSETTING
import pytest

def eq(x, y):
    return abs(x-y) < 1e-8


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
    assert eq(sol[x], -1)
    assert eq(sol[y], -2)

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
    print("solution: x* =", primal_sol[x], ", y* =", primal_sol[y], ", a* =", dual_sol[a], ", b* =", dual_sol[b])
    print("getDualSolVal: a* =", primal.getDualSolVal(c1), ", b* =", primal.getDualSolVal(c2))
    print("getDualsolLinear: a* =", primal.getDualsolLinear(c1), ", b* =", primal.getDualsolLinear(c2))
    print("dual")
    print(dual_sol[a], dual_sol[b])
    print(dual.getDualSolVal(d1), dual.getDualSolVal(d2))
    print(dual.getDualsolLinear(d1), dual.getDualsolLinear(d2))
    
    assert eq(primal_sol[x], 9)
    assert eq(primal_sol[y], 6)
    assert eq(primal.getDualSolVal(c2), dual_sol[b])
    assert eq(primal.getDualSolVal(c1), dual_sol[a])
    assert eq(dual.getDualSolVal(d1), primal_sol[x])
    assert eq(dual.getDualSolVal(d2), primal_sol[y])


    
def test_duals2():
    primal = Model()
    x1 = primal.addVar("x1", lb=0, ub=None)
    x2 = primal.addVar("x2", lb=0, ub=None)
    c1 = primal.addCons(5*x1 + 6*x2 == 7)
    primal.setObjective(3*x1 + 4*x2, sense="maximize")
    primal.setPresolve(SCIP_PARAMSETTING.OFF)
    primal.setHeuristics(SCIP_PARAMSETTING.OFF)
    primal.disablePropagation()
    primal.optimize()

    dual = Model()
    y1 = dual.addVar("y1", lb=None, ub=None)
    d1 = dual.addCons(5*y1 >= 3)
    d2 = dual.addCons(6*y1 >= 4)
    dual.setObjective(7*y1, sense="minimize")
    dual.setPresolve(SCIP_PARAMSETTING.OFF)
    dual.setHeuristics(SCIP_PARAMSETTING.OFF)
    dual.disablePropagation()
    dual.optimize()

    primal_sol = primal.getBestSol()
    dual_sol = dual.getBestSol()
    
    print("primal")
    print(primal_sol[x1], primal_sol[x2])
    print(primal.getDualSolVal(c1))
    print("dual")
    print(dual_sol[y1])
    print(dual.getDualSolVal(d1), dual.getDualSolVal(d2))
    
    assert eq(primal.getDualSolVal(c1), dual_sol[y1])
    # WARNING:
    # getting dual solution values using pyscipopt only works for
    # non-bound constraints, i.e. constraints containing at least two variables.
    # Currently, for active bound constraints, pyscipopt simply returns the bound
    # https://github.com/scipopt/PySCIPOpt/issues/136#issuecomment-420651298
    assert eq(dual.getDualSolVal(d1) / 5, primal_sol[x1])
    assert eq(dual.getDualSolVal(d2) / 6, primal_sol[x2])
