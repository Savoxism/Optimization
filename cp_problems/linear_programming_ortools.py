from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')
x3 = solver.NumVar(0, solver.infinity(), 'x3')
x4 = solver.NumVar(0, solver.infinity(), 'x4')
x5 = solver.NumVar(0, solver.infinity(), 'x5')
x6 = solver.NumVar(0, solver.infinity(), 'x6')

solver.Maximize(40*x1 + 10*x2 + 7*x5 + 14*x6)

solver.Add(x1 - x2 + 2*x5 == 0)
solver.Add(-2*x1 + x2 - 2 * x5 == 0)
solver.Add(x1 + x3 + x5 - x6 == 3)
solver.Add(x2 + x3 + x4 + 2 * x5 + x6 == 4)

status = solver.Solve()

# Step 6: Display the results
if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    print(x1.solution_value())
    print(x2.solution_value())
    print(x3.solution_value())
    print(x4.solution_value())
    print(x5.solution_value())
    print(x6.solution_value())
elif status == pywraplp.Solver.FEASIBLE:
    print('A feasible solution was found, but it might not be optimal.')
else:
    print('The problem does not have a feasible solution.')