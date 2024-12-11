import random

def generate_random_state(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def calculate_conflicts(state):
    violations = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j]:  # Same column
                violations += 1
            elif abs(state[i] - state[j]) == abs(i - j):  # Same diagonal
                violations += 1
    return violations

def generate_neighbors(state):
    neighbors = []
    n = len(state)
    for row in range(n):
        for col in range(n):
            if state[row] != col: 
                neighbor = state.copy()
                neighbor[row] = col
                neighbors.append(neighbor)
    return neighbors

def choose_best_neighbor(neighbors):
    best_neighbor = neighbors[0]
    best_violations = calculate_conflicts(best_neighbor)
    for neighbor in neighbors:
        violations = calculate_conflicts(neighbor)
        if violations < best_violations:
            best_neighbor = neighbor
            best_violations = violations
            
    return best_neighbor

def multistage_n_queens(n, max_restarts, max_iterations):
    for restart in range(max_restarts):
        state = generate_random_state(n)  # Start with a random state
        for iteration in range(max_iterations):
            violations = calculate_conflicts(state)
            
            if violations == 0:
                return state
            
            neighbors = generate_neighbors(state)
            next_state = choose_best_neighbor(neighbors)
            next_violations = calculate_conflicts(next_state)
            
            # Debug: Show the next state and its conflicts
            print(f"Next state: {next_state} with {next_violations} conflicts")
            
            # Stop if no improvement
            if calculate_conflicts(next_state) >= violations:
                break
        
            state = next_state  # Move to the next state
            
    return []  # No solution found

# Define the problem
n = 20
max_restarts = 100
max_iterations = 100

# Solve the problem
solution = multistage_n_queens(n, max_restarts, max_iterations)
print(f"\nFinal solution: {solution}")
