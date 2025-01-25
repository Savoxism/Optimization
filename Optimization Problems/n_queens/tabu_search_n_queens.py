import random

def generate_initial_solution(n):
    return [random.randint(0, n - 1) for _ in range(n)]

def calculate_conflicts(n, board):
    conflicts = 0
    for i in range(n):
        for j in range(i + 1, n):
            if board[i] == board[j]:
                conflicts += 1
            if abs(i - j) == abs(board[i] - board[j]):
                conflicts += 1
                
    return conflicts

def generate_neighbors(n, board):
    """Generate all neighbors by moving a queen in one row to a different column."""
    neighbors = []
    for row in range(n):
        for col in range(n):
            if board[row] != col:  # Only consider moves that change the position
                neighbor = board[:]
                neighbor[row] = col
                neighbors.append(neighbor)
    return neighbors
    
def tabu_search(n, max_iterations=1000, tabu_tenure=10):
    # Generate initial solution
    current_solution = generate_initial_solution(n)
    current_conflicts = calculate_conflicts(n, current_solution)
    
    best_solution = current_solution[:]
    best_conflicts = current_conflicts

    tabu_list = []  # List to store tabu moves
    iterations = 0
    
    while iterations < max_iterations and best_conflicts > 0:
        iterations += 1
        
        # Generate neighbors 
        neighbors = generate_neighbors(n, current_solution)
        neighbor_conflicts = [(neighbor, calculate_conflicts(n, neighbor)) for neighbor in neighbors]
        
        # Aspiration crirterion: conflicts < best_conflicts
        non_tabu_neighbors = [
            (neighbor, conflicts) for neighbor, conflicts in neighbor_conflicts 
            if neighbor not in tabu_list or conflicts < best_conflicts
        ]
        
        # Select the best neighbor
        best_neighbor, best_neighbor_conflicts = min(non_tabu_neighbors, key=lambda x: x[1])
        
        # Update tabu list
        tabu_list.append(current_solution)
        if len(tabu_list) > tabu_tenure:
            tabu_list.pop(0)
            
        current_solution = best_neighbor
        current_conflicts = best_neighbor_conflicts
        
        # Update global best solution
        if current_conflicts < best_conflicts:
            best_solution = current_solution[:]
            best_conflicts = current_conflicts
            
        # Print conflicts for each iteration for better illustration
        print(f"Iteration {iterations}: Current Conflicts = {current_conflicts}, Best Conflicts = {best_conflicts}")
            
    return best_solution, best_conflicts


n = int(input())
solution, conflicts = tabu_search(n)
print("Solution:", solution)
print("Conflicts:", conflicts)