import sys
from ortools.sat.python import cp_model

'''
7 18 2 1 0
2 1 115
6 5 175
6 2 200
4 3 149
6 1 155
5 6 179
0 4 125
4 1 124
2 3 155
5 4 107
4 2 172
6 4 175
4 6 103
1 6 121
3 2 132
3 6 103
4 0 197
2 0 138
2 1 0 4
5 6 4 3
'''

def read_input():
    lines = sys.stdin.readlines()

    n, m, k, s, t = map(int, lines[0].split())
    
    edges = []
    for i in range(1, m + 1):
        u, v, w = map(int, lines[i].split())
        edges.append((u, v, w))
    
    forbidden_pairs = []
    for i in range(m + 1, m + 1 + k):
        parts = lines[i].strip().split()
        start1, end1, start2, end2 = map(int, parts)
        forbidden_pairs.append(((start1, end1), (start2, end2))) 
        
    return n, m, k, s, t, edges, forbidden_pairs

def solve_cp(n, m, k, s, t, edges, forbidden_pairs):
    model = cp_model.CpModel()
    
    # Decision variables: x[i] = 1 if edge i is selected, 0 otherwise
    x = {}
    for i in range(m):
        x[i] = model.NewBoolVar(f'x_{i}')

    in_degree = {v: 0 for v in range(n)}
    out_degree = {v: 0 for v in range(n)}
    for i in range(m):
        u, v, w = edges[i]
        out_degree[u] += x[i]
        in_degree[v] += x[i]
        
    # Constraints for the start node (s)
    model.Add(out_degree[s] == 1)  
    model.Add(in_degree[s] == 0)   
    
    # Constraints for the end node (t)
    model.Add(out_degree[t] == 0)  
    model.Add(in_degree[t] == 1)   
    
    # Constraints for other nodes
    for v in range(n):
        if v != s and v != t:
            model.Add(in_degree[v] == out_degree[v])  
            model.Add(in_degree[v] <= 1)              
            model.Add(out_degree[v] <= 1)             
    
    edge_to_index = {(u, v): i for i, (u, v, _) in enumerate(edges)}
    for pair in forbidden_pairs:
        edge1, edge2 = pair
        # Get the indices of the edges in the forbidden pair
        idx1 = edge_to_index.get(edge1, -1)
        idx2 = edge_to_index.get(edge2, -1)
        
        if idx1 != -1 and idx2 != -1:
            model.Add(x[idx1] + x[idx2] <= 1)  
            
    # objective value
    total_cost = sum(x[i] * edges[i][2] for i in range(m))
    model.Minimize(total_cost)
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Extract the solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        return solver.ObjectiveValue()
    else:
        return -1
    


n, m, k, s, t, edges, forbidden_pairs = read_input()

cost = solve_cp(n, m, k, s, t, edges, forbidden_pairs)
print(cost)


