#PYTHON 
from ortools.sat.python import cp_model
import sys

def read_input():
    input = sys.stdin.read().splitlines()
    n_m = input[0].split()
    n = int(n_m[0])
    m = int(n_m[1])
    
    graph = [[] for _ in range(n + 1)]
    for i in range(1, m + 1):
        u_v_c = input[i].split()
        u = int(u_v_c[0])
        v = int(u_v_c[1])
        c = int(u_v_c[2])
        graph[u].append((v, c))
        graph[v].append((u, c))
    
    return n, m, graph

def solve(n, graph):
    model = cp_model.CpModel()
    
    first_path = {}
    second_path = {}
    
    for u, v, c in graph:
        first_path[(u, v)] = model.NewBoolVar(f"first_path_{u}_{v}")
        first_path[(v, u)] = model.NewBoolVar(f"first_path_{v}_{u}")
        second_path[(u, v)] = model.NewBoolVar(f"second_path_{u}_{v}")
        second_path[(v, u)] = model.NewBoolVar(f"second_path_{v}_{u}")
        
        for node in range(1, n + 1):
            if node == 1:
                model.Add(
                    sum(first_path[(1, v)] for v in range(1, n + 1) if (1, v) in first_path) - 
                    sum(first_path[(v, 1)] for v in range(1, n + 1) if (v, 1) in first_path) == 1
                )
            elif node == n:
                model.Add(
                    sum(first_path[(v, n)] for v in range(1, n + 1) if (v, n) in first_path) - 
                    sum(first_path[(n, v)] for v in range(1, n + 1) if (n, v) in first_path) == 1
                )
            else:
                model.Add(
                    sum(first_path[(v, node)] for v in range(1, n + 1) if (v, node) in first_path) - 
                    sum(first_path[(node, v)] for v in range(1, n + 1) if (node, v) in first_path) == 0
                )
                
        for node in range(1, n + 1):
            if node == 1:
                model.Add(
                    sum(second_path[(1, v)] for v in range(1, n + 1) if (1, v) in second_path) - 
                    sum(second_path[(v, 1)] for v in range(1, n + 1) if (v, 1) in second_path) == 1
                )
            elif node == n:
                model.Add(
                    sum(second_path[(v, n)] for v in range(1, n + 1) if (v, n) in second_path) - 
                    sum(second_path[(n, v)] for v in range(1, n + 1) if (n, v) in second_path) == 1
                )
            else:
                model.Add(
                    sum(second_path[(v, node)] for v in range(1, n + 1) if (v, node) in second_path) - 
                    sum(second_path[(node, v)] for v in range(1, n + 1) if (node, v) in second_path) == 0
                )
        
        # edge-disjoint constraint: each edge can be used in at most one path
        for u, v, c in graph:
            model.Add(first_path[(u, v)] + second_path[(u, v)] <= 1)
            model.Add(first_path[(v, u)] + second_path[(v, u)] <= 1)
            
        total_length = sum(
            c * (first_path[(u, v)] + second_path[(u, v)]) for u, v, c in graph)
        
        model.Minimize(total_length)
        
        solver = cp_model.CpSolver()
        status = solver.Solver(model)
        
        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            first_path_edges = [(u, v) for (u, v), var in first_path.items() if solver.Value(var) == 1]
            second_path_edges = [(u, v) for (u, v), var in second_path.items() if solver.Value(var) == 1]
            
            total_length = sum(c for u, v, c in graph if (u, v) in first_path_edges or (u, v) in second_path_edges)
            return total_length
        else:
            return "NOT_FEASIBLE"
        
if __name__ == "__main__":
    n, m, graph = read_input()
    result = solve(n, graph)
    print(result)
        
        
        
        
        
        