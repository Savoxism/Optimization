import random

def generate_initial_state(n):
    return [0] * n

def calculate_conflicts(state): # to compute the conflicts for all queens
    conflicts = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n): # consider rows after i 
            if state[i] == state[j]:  # Same column
                conflicts += 1
            elif abs(state[i] - state[j]) == abs(i - j):  # Same diagonal
                conflicts += 1
    return conflicts

def calculate_conflicts_for_queen(state, row): # to compute the conflicts for a specific queen
    conflicts = 0
    n = len(state)
    for other_row in range(n):
        if other_row != row:
            if state[other_row] == state[row]:  # Same column
                conflicts += 1
            elif abs(state[other_row] - state[row]) == abs(other_row - row):  # Same diagonal
                conflicts += 1
    return conflicts

def find_most_violating_queen(state):
    max_conflicts = 0
    most_violating_queen = []
    
    for row in range(len(state)): # For each queen
        conflicts = calculate_conflicts_for_queen(state, row)
        if conflicts > max_conflicts:
            max_conflicts = conflicts
            most_violating_queen = [row]
        elif conflicts == max_conflicts:
            most_violating_queen.append(row)
    
    return random.choice(most_violating_queen) # Break ties randomly

def find_best_position_for_queen(state, queen_row):
    n = len(state)
    min_conflicts = float('inf')
    best_positions = []
    
    # For each column
    for col in range(n):
        if state[queen_row] != col:  # Only consider moves
            new_state = state.copy()
            new_state[queen_row] = col
            conflicts = calculate_conflicts(new_state)
        
            if conflicts < min_conflicts:
                min_conflicts = conflicts
                best_positions = [col]
            elif conflicts == min_conflicts:
                best_positions.append(col)
                
    return random.choice(best_positions)  # Break ties randomly

def n_queens_local_search(n, max_iterations):
    state = generate_initial_state(n)
    for iteration in range(max_iterations):
        conflicts = calculate_conflicts(state)
        
        if conflicts == 0:
            return state  # Found a solution
        
        queen_row = find_most_violating_queen(state)
        best_position = find_best_position_for_queen(state, queen_row)
        state[queen_row] = best_position
        print(f"Iteration {iteration + 1}: State = {state}, Conflicts = {conflicts}")
        
    return []  # No solution found within max_iterations

# Solve the N-Queens problem
n = 200
max_iterations = 1000
solution = n_queens_local_search(n, max_iterations)
if solution:
    print(f"\nSolution found: {solution}")
else:
    print("\nNo solution found.")