from ortools.sat.python import cp_model

def solve(grid):
    model = cp_model.CpModel()
    
    n = 9
    cells = range(n)
    x = [[model.NewIntVar(1, n, f'x[{row}][{col}]') for col in cells] for row in cells]
    
    # Row constraints
    for row in cells:
        model.AddAllDifferent(x[row])
    
    # Column constraints
    for col in cells:
        model.AddAllDifferent([x[row][col] for row in cells])
        
    # Subgrid constraints
    sub_grid_size = 3
    for box_row in range(0, n, sub_grid_size):
        for box_col in range(0, n, sub_grid_size):
            model.AddAllDifferent([x[box_row + i][box_col + j] for i in range(sub_grid_size) for j in range(sub_grid_size)])
            
    # add constraints for the pre-filled cells
    for row in cells:
        for col in cells:
            if grid[row][col] != 0:
                model.Add(x[row][col] == grid[row][col])
                
    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Display the solution if found
    if status == cp_model.FEASIBLE or status == cp_model.OPTIMAL:
        solution = [[solver.Value(x[row][col]) for col in cells] for row in cells]
        for row in solution:
            print(row)
        return solution
    else:
        print("No solution found.")
        return None

# Example Sudoku puzzle (0 represents empty cells)
sudoku_grid = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

solve(sudoku_grid)