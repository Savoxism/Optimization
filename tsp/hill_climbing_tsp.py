import sys
import random

def read_input():
    n = int(sys.stdin.readline().strip())
    cost_matrix = []
    
    for _ in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        cost_matrix.append(row)
        
    return n, cost_matrix

def generate_initial_solution(n):
    return random.sample(range(n), n)

def calculate_total_cost(n, cost_matrix, route):
    total_cost = sum(cost_matrix[route[i]][route[i + 1]] for i in range(n - 1))
    total_cost += cost_matrix[route[-1]][route[0]]
    return total_cost

def get_neighbors(route):
    neighbors = []
    for i in range(len(route)):
            for j in range(i + 1, len(route)):
                neighbor = route[:]
                neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
                neighbors.append(neighbor)
    return neighbors

def get_random_neighbor(route):
        """Generate a random neighbor by swapping two cities."""
        neighbor = route[:]
        i, j = random.sample(range(len(route)), 2)
        neighbor[i], neighbor[j] = neighbor[j], neighbor[i]
        return neighbor

def hill_climbing(n, cost_matrix, max_iterations=1000):
    current_solution = generate_initial_solution(n) 
    current_cost = calculate_total_cost(n, cost_matrix, current_solution)
    
    best_solution = current_solution[:]
    best_cost = current_cost
    
    iterations = 0
    
    while iterations < max_iterations:
        iterations += 1
        
        # Step 3: Select a random neighbor
        neighbor = get_random_neighbor(current_solution)
        neighbor_cost = calculate_total_cost(n, cost_matrix, neighbor)

        
        # Step 4: Accept neighbor if it improves the solution
        if neighbor_cost < current_cost:
            current_solution = neighbor
            current_cost = neighbor_cost

            # Update the best solution if the neighbor is better
            if current_cost < best_cost:
                best_solution = current_solution[:]
                best_cost = current_cost

    return best_solution, best_cost

if __name__ == "__main__":
    n, cost_matrix = read_input()
    best_solution, best_cost = hill_climbing(n, cost_matrix)
    
    print(best_cost)
    print(" ".join(str(city) for city in best_solution))