from ortools.sat.python import cp_model

def solve_path_with_forbidden_pairs(n, m, k, s, t, edges, forbidden_pairs):
    # Initialize the CP-SAT model
    model = cp_model.CpModel()

    # Decision variables: x[e] = 1 if edge e is in the path, else 0
    x = {}
    for idx, (u, v, cost) in enumerate(edges):
        x[idx] = model.NewBoolVar(f'x[{idx}]')

    # Constraint 1: Path starts at s and ends at t
    # Flow conservation constraints to ensure connectivity
    # For each node, the number of incoming edges equals the number of outgoing edges, except for s and t
    flow = {}
    for node in range(n):
        if node == s:
            # Source node: out-degree = 1, in-degree = 0
            model.Add(sum(x[idx] for idx, (u, _, _) in enumerate(edges) if u == node) == 1)
            model.Add(sum(x[idx] for idx, (_, v, _) in enumerate(edges) if v == node) == 0)
        elif node == t:
            # Target node: in-degree = 1, out-degree = 0
            model.Add(sum(x[idx] for idx, (_, v, _) in enumerate(edges) if v == node) == 1)
            model.Add(sum(x[idx] for idx, (u, _, _) in enumerate(edges) if u == node) == 0)
        else:
            # Intermediate nodes: in-degree = out-degree
            model.Add(sum(x[idx] for idx, (u, _, _) in enumerate(edges) if u == node) ==
                      sum(x[idx] for idx, (_, v, _) in enumerate(edges) if v == node))

    # Constraint 2: Elementary path (each node is visited at most once)
    # Ensure that the path does not revisit any node
    for node in range(n):
        model.Add(sum(x[idx] for idx, (u, _, _) in enumerate(edges) if u == node) <= 1)

    # Constraint 3: Forbidden edge pairs
    # Ensure that no two edges in a forbidden pair are included in the path
    for (e1_start, e1_end, e2_start, e2_end) in forbidden_pairs:
        e1_idx = next((idx for idx, (u, v, _) in enumerate(edges) if u == e1_start and v == e1_end), None)
        e2_idx = next((idx for idx, (u, v, _) in enumerate(edges) if u == e2_start and v == e2_end), None)
        if e1_idx is not None and e2_idx is not None:
            model.Add(x[e1_idx] + x[e2_idx] <= 1)

    # Objective: Minimize the total cost of the path
    total_cost = sum(x[idx] * cost for idx, (_, _, cost) in enumerate(edges))
    model.Minimize(total_cost)

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Extract the path
        path_edges = [idx for idx in x if solver.Value(x[idx])]
        total_cost_value = sum(edges[idx][2] for idx in path_edges)
        return total_cost_value
    else:
        return -1

# Example usage
n = 7  # Number of nodes
m = 18  # Number of edges
k = 2  # Number of forbidden pairs
s = 1  # Source node
t = 0  # Target node

# List of edges: (u, v, cost)
edges = [
    (2, 1, 115),
    (6, 5, 175),
    (6, 2, 200),
    (4, 3, 149),
    (6, 1, 155),
    (5, 6, 179),
    (0, 4, 125),
    (4, 1, 124),
    (2, 3, 155),
    (5, 4, 107),
    (4, 2, 172),
    (6, 4, 175),
    (4, 6, 103),
    (1, 6, 121),
    (3, 2, 132),
    (3, 6, 103),
    (4, 0, 197),
    (2, 0, 138)
]

# List of forbidden pairs: (e1_start, e1_end, e2_start, e2_end)
forbidden_pairs = [
    (2, 1, 0, 4),
    (5, 6, 4, 3)
]

# Solve the problem
result = solve_path_with_forbidden_pairs(n, m, k, s, t, edges, forbidden_pairs)
print("Total cost of the path:", result)