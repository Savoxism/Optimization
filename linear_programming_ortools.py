from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

x = solver.NumVar(0.0, solver.infinity(), 'x')
y = solver.NumVar(0.0, solver.infinity(), 'y')

solver.Add(x + 2 * y <= 14.0)
solver.Add(3 * x - y >= 0.0)
solver.Add(x - y <= 2.0)

solver.Maximize(3 * x + 4 * y)

status = solver.Solve()

# Step 6: Display the results
if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    print('x =', x.solution_value())
    print('y =', y.solution_value())
elif status == pywraplp.Solver.FEASIBLE:
    print('A feasible solution was found, but it might not be optimal.')
else:
    print('The problem does not have a feasible solution.')