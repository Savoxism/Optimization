import sys
from ortools.sat.python import cp_model
'''
Subtour elimination: If a path between two cities is included in the tour, the positions of these cities must be consistent with the distance between them.

In the context of the Traveling Salesman Problem (TSP), the last city in the tour should be the one that connects back to the starting city to complete the tour.
'''
    
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
    
    # Calculate upper bound for y variables = sum of all distances
    upper_bound = sum(sum(row) for row in cost_matrix) 

    # Initialize sets for incoming and outgoing connections
    incoming = [set(range(num_cities + 1)) for _ in range(num_cities + 1)]
    outgoing = [set(range(num_cities + 1)) for _ in range(num_cities + 1)]
    
    model = cp_model.CpModel()
    
    # Decision variables
    x = {}
    for i in range(num_cities + 1):
        for j in outgoing[i]:
            x[i, j] = model.NewIntVar(0, 1, f"x({i},{j})")
    
    # y[i] represents the position of city i (distance from starting city to citi[i]) in the tour (0 <= y[i] <= D)        
    y = [model.NewIntVar(0, upper_bound, f"y({i})") for i in range(num_cities + 1)]
    
    # constraint 1: each city is visited exactly once
    for i in range(num_cities):
        model.Add(sum(x[i, j] for j in outgoing[i]) == 1)
        
    # constraint 2: each city is left exactly once
    for i in range(1, num_cities + 1):
        model.Add(sum(x[j, i] for j in incoming[i]) == 1)
        
    # constraint 3: self-loop is not allowed
    for i in range(num_cities + 1):
        model.Add(x[i, i] == 0)
        
    # constraint 4: starting city position constraint
    model.Add(y[0] == 0) 
    
    # constraing 5: subtour elimination
    for i in range(num_cities + 1):
        for j in range(num_cities + 1):
            b = model.NewBoolVar('')
            # These 2 constraints ensure that b is true if and only is the path from i to j is included in the tour
            model.Add(x[i, j] == 1).OnlyEnforceIf(b)
            model.Add(x[i, j] != 1).OnlyEnforceIf(b.Not())
            # if the path from i to j is included in the tour, the position of city j must be equal to the position of city i plus the distance between them
            model.Add(y[i] + cost_matrix[i][j] == y[j]).OnlyEnforceIf(b)
            
    # Objective function
    model.Minimize(y[num_cities])
    
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = 5.0
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(solver.Value(y[num_cities]))
        for i in range(num_cities + 1):
            for j in range(num_cities + 1):
                if solver.Value(x[i, j]) > 0:
                    print(f"x[{i}, {j}] = {solver.Value(x[i, j])}")
                    
        for i in range(num_cities + 1):
            print(f"y({i}) = {solver.Value(y[i])}") 
    else: 
        print("No solution found")
        
        
if __name__ == "__main__":
    solve_tsp()