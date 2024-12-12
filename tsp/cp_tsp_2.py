import sys
from ortools.sat.python import cp_model

def read_input():
    n = int(sys.stdin.readline().strip())
    cost_matrix = []
    for _ in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        row.append(row[0])
        cost_matrix.append(row)
    cost_matrix.append(cost_matrix[0])
    return n, cost_matrix 

def solve_tsp():
    num_cities, cost_matrix = read_input()
    
    upper_bound = sum(max(row) for row in cost_matrix)
    
    model = cp_model.CpModel()
    
    x = [model.NewIntVar(0, num_cities, f"x[{i}]") for i in range(num_cities)]
    y = [model.NewIntVar(0, upper_bound, f"y[{i}]") for i in range(num_cities + 1)]
    
    # Constraint 1: Each city is visited exactly once
    for i in range(num_cities):
        for j in range(i + 1, num_cities):
            model.Add(x[i] != x[j])
            
    # Constraint 2: no self-loop
    for i in range(num_cities):
        model.Add(x[i] != i)
        
    # Constraint 3: starting city position constraint
    model.Add(y[0] == 0)
    
    # constraint 4: subtour elimination
    for i in range(num_cities):
        for j in range(num_cities + 1):
            b = model.NewBoolVar('')
            model.Add(x[i] == j).OnlyEnforceIf(b)
            model.Add(x[i] != j).OnlyEnforceIf(b.Not())
            model.Add(y[i] + cost_matrix[i][j] == y[j]).OnlyEnforceIf(b)
    
    model.Minimize(y[num_cities])
    
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5.0
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(solver.Value(y[num_cities]))
    else:
        print('No solution found')
        
        
if __name__ == "__main__":
    solve_tsp()