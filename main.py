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
    
    # Calculate upper bound for y variables
    upper_bound = sum(sum(row) for row in cost_matrix)
    
    # Initialize sets for incoming and outgoing connections
    incoming = [set(range(num_cities + 1)) for _ in range(num_cities + 1)]
    outgoing = [set(range(num_cities + 1)) for _ in range(num_cities + 1)]
    
    # Create the model
    model = cp_model.CpModel()
    
    # Decision variables
    x = {}
    for i in range(num_cities + 1):
        for j in outgoing[i]:
            x[i, j] = model.NewIntVar(0, 1, f"x({i},{j})")
    
    y = [model.NewIntVar(0, upper_bound, f"y({i})") for i in range(num_cities + 1)]
    
    # Constraints
    for i in range(num_cities):
        model.Add(sum(x[i, j] for j in outgoing[i]) == 1)
    
    for i in range(1, num_cities + 1):
        model.Add(sum(x[j, i] for j in incoming[i]) == 1)
    
    for i in range(num_cities + 1):
        model.Add(x[i, i] == 0)
    
    model.Add(y[0] == 0)
    
    for i in range(num_cities + 1):
        for j in range(num_cities + 1):
            b = model.NewBoolVar('')
            model.Add(x[i, j] == 1).OnlyEnforceIf(b)
            model.Add(x[i, j] != 1).OnlyEnforceIf(b.Not())
            model.Add(y[i] + cost_matrix[i][j] == y[j]).OnlyEnforceIf(b)
    
    # Objective function
    model.Minimize(y[num_cities])
    
    # Solve the model
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5.0
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(solver.Value(y[num_cities]))
        print('Objective value:', solver.Value(y[num_cities]))
        for i in range(num_cities + 1):
            for j in range(num_cities + 1):
                if solver.Value(x[i, j]) > 0:
                    print(f"x[{i}, {j}] = {solver.Value(x[i, j])}")
        
        for i in range(num_cities + 1):
            print(f"y[{i}] = {solver.Value(y[i])}")
            
    else:
        print("No solution found")

if __name__ == "__main__":
    solve_tsp()