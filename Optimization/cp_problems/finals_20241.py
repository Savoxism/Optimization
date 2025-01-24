import sys 
from ortools.sat.python import cp_model
"""
6 7
1 2
1 3
2 3
2 4
3 4
4 5
5 6
"""
def read_input():
    input = sys.stdin.read().splitlines()
    n, m = map(int, input[0].split())
    
    graph = [[] for _ in range(n)]
    for line in input[1:]:
        u, v = map(int, line.split())
        graph[u - 1].append(v - 1)
        graph[v - 1].append(u - 1)
    
    return n, graph
    
def solve(n, graph):
    model = cp_model.CpModel()
    max_colors = n
    
    # Color of each node 
    x = [model.NewIntVar(0, max_colors - 1, f"x{i}") for i in range(n)]
    
    for u in range(n):
        for v in graph[u]:
            if u < v: 
                model.Add(x[u] != x[v])
       
    max_color = model.NewIntVar(0, max_colors - 1, "max_color")
    model.AddMaxEquality(max_color, x)
    model.Minimize(max_color) 
            
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(solver.Value(max_color) + 1)  
        solution = [solver.Value(i) + 1 for i in x] 
        print(" ".join(map(str, solution)))
    else:
        print("INFEASIBLE")

if __name__ == "__main__":
    n, graph = read_input()
    solve(n, graph)