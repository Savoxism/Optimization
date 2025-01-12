import sys
from ortools.sat.python import cp_model

'''
4 
0 1 1 9
1 0 9 3
1 9 0 2
9 3 2 0
'''

def read_input():
    input = sys.stdin.read().splitlines()
    n = int(input[0])
    
    cost_matrix = []
    
    for row in input[1:]:
        row = [int(x) for x in row.split()]
        cost_matrix.append(row)
        
    cost_matrix.remove(cost_matrix[-1])
    
    return n, cost_matrix 

def solve(n, cost_matrix):
    model = cp_model.CpModel()
    
    # decision variables
    x = {}
    for i in range(n):
        for j in range(n):
            if i != j:
                x[i, j] = model.NewBoolVar(f"x_{i}_{j}")
    
    # Subtour elimination variables
    y = [model.NewIntVar(0, n - 1, f"y_{i}") for i in range(n)]
    
    # each city is visited once only 
    for i in range(n):
        model.Add(sum(x[i, j] for j in range(n) if i != j) == 1) 
        model.Add(sum(x[j, i] for j in range(n) if i != j) == 1) 
        
    # subtour
    for i in range(1, n):
        for j in range(1, n):
            if i != j:
                b = model.NewBoolVar(f"b_{i}_{j}")
                # These 2 constraints ensure that b is true if and only if the path from i to j is included in the tour
                model.Add(x[i, j] == 1).OnlyEnforceIf(b)
                model.Add(x[i, j] != 1).OnlyEnforceIf(b.Not())
                # If the path from i to j is included in the tour, the position of city j must be equal to the position of city i plus 1
                model.Add(y[i] + 1 == y[j]).OnlyEnforceIf(b)
                
    objective = sum(cost_matrix[i][j] * x[i, j] for i in range(n) for j in range(n) if i != j)
    model.Minimize(objective)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(int(solver.ObjectiveValue()))
    else:
        print("INFEASIBLE")
    
if __name__ == "__main__":
    n, cost_matrix = read_input()
    solve(n, cost_matrix)














