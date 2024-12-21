from ortools.sat.python import cp_model

model = cp_model.CpModel()

x0 = model.NewIntVar(1, 5, 'x0')
x1 = model.NewIntVar(1, 5, 'x1')
x2 = model.NewIntVar(1, 5, 'x2')
x3 = model.NewIntVar(1, 5, 'x3')
x4 = model.NewIntVar(1, 5, 'x4')

model.Add(x2 + 3 != x1)
model.Add(x3 <= x4)
model.Add(x2 + x3 == x0 + 1)
model.Add(x4 <= 3)
model.Add(x1 + x4 == 7)

b = model.NewBoolVar('b')
model.Add(x2 == 1).OnlyEnforceIf(b)
model.Add(x2 != 1).OnlyEnforceIf(b.Not())
model.Add(x4 != 2).OnlyEnforceIf(b)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL:
    print("Maximum of objective function %i" % solver.ObjectiveValue())
    print()
    print('x0 =', solver.Value(x0))
    print('x1 =', solver.Value(x1))
    print('x2 =', solver.Value(x2))
    print('x3 =', solver.Value(x3))
    print('x4 =', solver.Value(x4))