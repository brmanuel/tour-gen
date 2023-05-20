
from pyscipopt import Model
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
    pass

