from ortools.linear_solver import pywraplp

solver = pywraplp.Solver.CreateSolver('GLOP')

x1 = solver.NumVar(0, solver.infinity(), 'x1')
x2 = solver.NumVar(0, solver.infinity(), 'x2')
x3 = solver.NumVar(0, solver.infinity(), 'x3')


solver.Maximize(3*x1 + 2*x2 - 7*x3)

solver.Add(2*x1 - 3*x2 + x3 <= 4)
solver.Add(x1 - x2 <= 7)
solver.Add(3*x1 - 2*x2 + 6*x3  <= 10)


status = solver.Solve()

# Step 6: Display the results
if status == pywraplp.Solver.OPTIMAL:
    print('Solution:')
    print('Objective value =', solver.Objective().Value())
    print(x1.solution_value())
    print(x2.solution_value())
    print(x3.solution_value())
elif status == pywraplp.Solver.FEASIBLE:
    print('A feasible solution was found, but it might not be optimal.')
else:
    print('The problem does not have a feasible solution.')