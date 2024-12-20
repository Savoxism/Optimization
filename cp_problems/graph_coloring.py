from ortools.sat.python import cp_model

def solve(graph):
    model = cp_model.CpModel()
    
    num_nodes = len(graph)
    nodes = range(num_nodes)
    
    # The colors are integers starting from 0
    colors = [model.NewIntVar(0, num_nodes - 1, f'color[{node}]') for node in nodes]
    
    # Constraint: adjacent nodes must have different colors
    
    for node, neighbors in enumerate(graph):
        for neighbor in neighbors:
            if node < neighbor:
                model.Add(colors[node] != colors[neighbor]) # adjacent nodes must have different colors
                
    max_color = model.NewIntVar(0, num_nodes - 1, 'max_color')
    model.AddMaxEquality(max_color, colors)
    model.Minimize(max_color)
    
    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output the results
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print(f"Minimum number of colors used: {solver.Value(max_color) + 1}")
        solution = {node: solver.Value(colors[node]) for node in nodes}
        for node, color in solution.items():
            print(f"Node {node} -> Color {color}")
        return solution
    else:
        print("No solution found.")
        return None

example_graph = [
    [1, 2],        # Neighbors of Node 0
    [0, 2, 3],     # Neighbors of Node 1
    [0, 1, 3],     # Neighbors of Node 2
    [1, 2]         # Neighbors of Node 3
]

solve(example_graph)