from ortools.sat.python import cp_model
import sys


def read_input():
    lines = sys.stdin.readlines()
    no_nodes, no_edges = map(int, lines[0].split())

    edges = []
    for i in range(1, no_edges + 1):
        u, v, w = map(int, lines[i].split())
        edges.append((u, v, w))

    return no_nodes, edges


def solve(no_nodes, edges, s, t):
    model = cp_model.CpModel()
    
    x = {}
    y = {}
    for u, v, _ in edges:
        x[(u, v)] = model.NewBoolVar(f"x[{u},{v}]")
        y[(u, v)] = model.NewBoolVar(f"y[{u},{v}]")
        
    # Constraint 1: flow conservation
    for node in range(1, no_nodes + 1):
        if node == s or node == t:
            continue
        
        # First path flow conservation
        model.Add(
            sum(x[(u, v)] for u, v, _ in edges if u == node) ==
            sum(x[(v, u)] for v, u, _ in edges if u == node)
        )

        # Second path flow conservation
        model.Add(
            sum(y[(u, v)] for u, v, _ in edges if u == node) ==
            sum(y[(v, u)] for v, u, _ in edges if u == node)
        )
        
    # Constraint 2: Start and end
    model.Add(sum(x[(s, v)] for node, v, _ in edges if s == node) == 1)
    model.Add(sum(y[(s, v)] for node, v, _ in edges if s == node) == 1)
    model.Add(sum(x[(v, t)] for v, node, _ in edges if t == node) == 1)
    model.Add(sum(y[(v, t)] for v, node, _ in edges if t == node) == 1)
    
    # Constraint 3: Disjoint paths
    for u, v, w in edges:
        model.Add(x[(u, v)] + y[(u, v)] <= 1)
        
    # Objective function
    model.Minimize(
        sum(w * x[(u, v)] for u, v, w in edges) +
        sum(w * y[(u, v)] for u, v, w in edges)
    )
    
    # Initalize solver
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL:
        print(int(solver.ObjectiveValue()))

        # print("First path edges:")
        # for u, v, _ in edges:
        #     if solver.Value(x[(u, v)]) == 1:
        #         print(f"({u}, {v})")

        # print("Second path edges:")
        # for u, v, _ in edges:
        #     if solver.Value(y[(u, v)]) == 1:
        #         print(f"({u}, {v})")
    else:
        print("NOT_FEASIBLE")
        
if __name__ == "__main__":
    no_nodes, edges = read_input()
    solve(no_nodes=no_nodes, edges=edges, s=1, t=no_nodes)