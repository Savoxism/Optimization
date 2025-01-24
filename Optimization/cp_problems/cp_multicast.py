import sys
from ortools.sat.python import cp_model

'''
7 12 1 6
1 2 2 10
1 3 6 4
1 4 1 5
2 3 4 9
2 6 5 1
2 7 2 3
3 4 8 9
3 5 6 2
3 6 8 7
4 5 3 5
5 6 1 4
6 7 4 5
'''
def read_input():
    input = sys.stdin.read().splitlines()
    
    n, m, s, L = map(int, input[0].split())
    
    edges = []
    for line in input[1:]:
        u, v, t, c = map(int, line.split())
        edges.append((u, v, t, c))
        
    return n, m, s, L, edges

def solve(n, m, s, L, edges):
    time_and_cost = {}
    
    neighborhood = {}
    for u, v, t, c in edges:
        u -= 1
        v -= 1
        time_and_cost[(u, v)] = (t, c)
        
        if u not in neighborhood:
            neighborhood[u] = []
            
        neighborhood[u].append(v)
        
    # Build incoming neighbors dictionary - map nodes to their parents
    In = {}
    for u in neighborhood:
        for v in neighborhood[u]:
            if v not in In:
                In[v] = []
            In[v].append(u)

    # Create the CP model
    model = cp_model.CpModel()
    
    x = [model.NewIntVar(0, n - 1, f"x{i}") for i in range(n)] # parent of node i
    y = [model.NewIntVar(0, 5500, f"y{i}") for i in range(n)] # time to reach node i from s
    z = {edge: model.NewIntVar(0, 1, f"z{edge[0]}_{edge[1]}") for edge in time_and_cost} # A binary variable indicating whether the edge (i, j) is used in the solution
    
    # Constraints
    # 1. Source node has time 0
    model.Add(y[s - 1] == 0)
    
    # 2. Parent assignment constraint 
    for i in range(n):
        if i != s - 1:
            model.AddAllowedAssignments([x[i]], [[v] for v in In[i]])
            
    # 3. Edge activation and time computation
    for i in range(n):
        if i != s - 1:
            for j in In[i]:
                condition_met = model.NewBoolVar(f"condition_met_{j}_{i}")
                # if a node i has parent j 
                model.Add(x[i] == j).OnlyEnforceIf(condition_met) 
                model.Add(z[(j, i)] == 1).OnlyEnforceIf(condition_met)
                model.Add(y[j] + time_and_cost[(j, i)][0] == y[i]).OnlyEnforceIf(condition_met)
                # if a node i does not have parent j
                model.Add(x[i] != j).OnlyEnforceIf(condition_met.Not())
                model.Add(z[(j, i)] == 0).OnlyEnforceIf(condition_met.Not())
    
    # 4. Time constraint
    for j in range(n):
        model.Add(y[j] <= L)

    objective = sum(z[edge] * time_and_cost[edge][1] for edge in time_and_cost)
    model.Minimize(objective)

    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL:
        print(int(solver.ObjectiveValue()))
    else:
        print("NO_SOLUTION")
        
if __name__ == "__main__":
    n, m, s, L, edges = read_input()
    solve(n, m, s, L, edges)
    