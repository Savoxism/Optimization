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
    '''
    n: number of nodes
    m: number of edges
    k; number of forbidden pairs
    s: source node
    t: target node
    '''
    input = sys.stdin.read()
    lines = input.split('\n')
    n, m, k, s, t = map(int, lines[0].split())
    
    edges = []
    for i in range(m):
        u, v, cost = map(int, lines[i+1].split())
        
        edges.append((u, v, cost))
        
    forbidden_pairs = []
    for i in range(k):
        e1_start, e1_end, e2_start, e2_end = map(int, lines[m+i+1].split())
        
        forbidden_pairs.append((e1_start, e1_end, e2_start, e2_end))
        
    return n, m, k, s, t, edges, forbidden_pairs

def solve(n, m, k, s, t, edges, forbidden_pairs):
    model = cp_model.CpModel()
    
    # Decision variables: x[e] = 1 if edge e is in the path, else 0
    x = {}
    for idx, (u, v, cost) in enumerate(edges):
        x[idx] = model.NewBoolVar(f'x_{idx}')
        
    # constraint 1: every node considered has at most one incoming and one outgoing edge except for the source and target nodes
    for node in range(n):
        if node == s:
            model.Add(sum(x[idx] for idx, (u, _, _) in enumerate(edges) if u == node) == 1)
            model.Add(sum(x[idx] for idx, (_, v, _) in enumerate(edges) if v == node) == 0)
        elif node == t:
            model.Add(sum(x[idx] for idx, (u, _, _) in enumerate(edges) if u == node) == 0)
            model.Add(sum(x[idx] for idx, (_, v, _) in enumerate(edges) if v == node) == 1)
        else:
            model.Add(sum(x[idx] for idx, (u, _, _) in enumerate(edges) if u == node) == sum(x[idx] for idx, (_, v, _) in enumerate(edges) if v == node))
        
    # Constraint 2: no two edges in a forbidden pair are included in the path
    for (e1_start, e1_end, e2_start, e2_end) in forbidden_pairs:
        e1_idx = next((idx for idx, (u, v, _) in enumerate(edges) if u == e1_start and v == e1_end), None)
        e2_idx = next((idx for idx, (u, v, _) in enumerate(edges) if u == e2_start and v == e2_end), None)
        if e1_idx is not None and e2_idx is not None:
            model.Add(x[e1_idx] + x[e2_idx] <= 1)
    
    model.Minimize(sum(x[idx] * cost for idx, (_, _, cost) in enumerate(edges)))
    
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        path_edges = [idx for idx in x if solver.Value(x[idx])]
        total_cost = sum(edges[idx][2] for idx in path_edges)
        return total_cost
    else:
        return -1
    
if __name__ == '__main__':
    n, m, k, s, t, edges, forbidden_pairs = read_input()
    result = solve(n, m, k, s, t, edges, forbidden_pairs)
    print(result)
