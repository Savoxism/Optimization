import sys
from ortools.linear_solver import pywraplp

def read_input():
    n = int(sys.stdin.readline().strip())
    cost_matrix = []
    for _ in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        cost_matrix.append(row)
    return n, cost_matrix

# Find subtours in the current solution
def check_subtours(x_val, n):
    visited = set()
    subtours = []
    
    for i in range(n):
        if i not in visited:
            current = i
            subtour = []
            
            while True:
                visited.add(current)
                subtour.append(current)
                next_city = None
                for j in range(n):
                    if x_val[current][j] == 1:
                        next_city = j
                        break
                if next_city is None or next_city in visited:
                    break
                current = next_city
                
            if len(subtour) < n:
                subtours.append(subtour)
    
    return subtours

def solve_tsp(n, cost_matrix):
    # Setup solver
    solver = pywraplp.Solver.CreateSolver('SCIP')
    if not solver:
        print('Solver not found')
        return 
    
    # Decision variables
    x = [[solver.IntVar(0, 1, f'x[{i},{j}]') for j in range(n)] for i in range(n)]
    
    # Constraints: each city has exactly one incoming edge and outgoing edge
    for i in range(n):
        solver.Add(solver.Sum(x[i][j] for j in range(n) if i != j) == 1)
        solver.Add(solver.Sum(x[j][i] for j in range(n) if i != j) == 1)
    
    # Objective function: minimize total cost
    solver.Minimize(solver.Sum(cost_matrix[i][j] * x[i][j] for i in range(n) for j in range(n)))
    
    # Solve initially without subtour elimination constraints
    solver.Solve()
    
    # Check for subtours
    while True:
        # Get the current solution
        x_val = [[x[i][j].solution_value() for j in range(n)] for i in range(n)]
        
        # Check for subtours in the solution
        subtours = check_subtours(x_val, n)
        if not subtours:
            break  # valid solution found
        
        # Add subtour elimination constraints
        for subtour in subtours:
            solver.Add(
                solver.Sum(x[i][j] for i in subtour for j in subtour if i != j) <= len(subtour) - 1
            )

        # Re-solve with the new constraints
        solver.Solve()
        
    # Extract the final tour
    current_city = 0
    tour = [current_city + 1]  # Convert to 1-based indexing
    for _ in range(n - 1):
        for j in range(n):
            if x_val[current_city][j] == 1:
                tour.append(j + 1)  # Convert to 1-based indexing
                current_city = j
                break
    
    # Output the results in the desired format
    print(n)
    print(" ".join(map(str, tour)))

if __name__ == "__main__":
    n, cost_matrix = read_input()
    solve_tsp(n, cost_matrix)
