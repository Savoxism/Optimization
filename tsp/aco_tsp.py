import sys
import random
import math

def read_input():
    n = int(sys.stdin.readline().strip())
    cost_matrix = []
    
    for _ in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        cost_matrix.append(row)
        
    return n, cost_matrix

def initialize_matrices(n, cost_matrix):
    pheromone_matrix = [[1 for _ in range(n)] for _ in range(n)]
    
    visibility_matrix = [[1 / cost_matrix[i][j] if i != j else 0 for j in range(n)] for i in range(n)]
    
    return pheromone_matrix, visibility_matrix
    
def generate_initial_solution(n, pheromone_matrix, visibility_matrix, alpha=1, beta=2):
    all_tours = []
    
    for start_city in range(n):
        tour = [start_city]
        visited = set(tour)
        
        while len(tour) < n:
            current_city = tour[-1]
            unvisited = [city for city in range(n) if city not in visited]
            next_city = select_next_city(current_city, unvisited, pheromone_matrix, visibility_matrix, alpha, beta)
            tour.append(next_city)
            visited.add(next_city)

        # Complete the tour by returning to the start city
        tour.append(tour[0])
        all_tours.append(tour)

    return all_tours

def select_next_city(current_city, unvisited, pheromone_matrix, visibility_matrix, alpha=1, beta=2):
    probabilities = []
    
    # Calculate the probability of moving to each city
    for next_city in unvisited:
        pheromone = pheromone_matrix[current_city][next_city]
        visibility = visibility_matrix[current_city][next_city]
        
        probability = math.pow(pheromone, alpha) * math.pow(visibility, beta)    
        probabilities.append((next_city, probability))
        
    sigma_probs = sum(prob for _ , prob in probabilities)
    
    probabilities = [(city, prob / sigma_probs) for city, prob in probabilities]
    
    # Roulette wheel selection
    next_city = random.choices(
        population=[city for city, _ in probabilities],
        weights=[prob for _, prob in probabilities],
    )[0]
    
    return next_city

def two_opt(tour, cost_matrix):
    n = len(tour)
    best_gain = 0
    best_tour = tour[:]
    
    for i in range(1, n - 2):
        for j in range(i + 1, n - 1):
            # Calculate gain from swapping edges (i-1, i) and (j, j+1)
            gain = (
                cost_matrix[tour[i - 1]][tour[j]] +
                cost_matrix[tour[i]][tour[j + 1]] -
                cost_matrix[tour[i - 1]][tour[i]] -
                cost_matrix[tour[j]][tour[j + 1]]   
            )
            
            if gain < 0:
                best_gain = gain
                best_tour = tour[:i] + tour[i:j + 1][::-1] + tour[j + 1:]
                
    return best_tour if best_gain < 0 else tour
    
def ACO(n, cost_matrix, alpha=1, beta=2, p=0.1, q=100, iterations=100):
    pheromone_matrix, visibility_matrix = initialize_matrices(n, cost_matrix)
    best_tour = None
    best_cost = float('inf')
    
    for iteration in range(iterations):
        # Generate initial solutions
        solutions = generate_initial_solution(n, pheromone_matrix, visibility_matrix, alpha, beta)
        
        # Apply 2-opt to improve each solution
        improved_solutions = []
        for tour in solutions:
            improved_tour = two_opt(tour, cost_matrix)
            improved_solutions.append(improved_tour)

        # Evaluate solutions
        solution_costs = [sum(cost_matrix[tour[i]][tour[i + 1]] for i in range(len(tour) - 1)) for tour in improved_solutions]
        iteration_best_cost = min(solution_costs)
        iteration_best_tour = improved_solutions[solution_costs.index(iteration_best_cost)]
        
        if iteration_best_cost < best_cost:
            best_cost = iteration_best_cost
            best_tour = iteration_best_tour
            
        # Debug: Print reduction in distance
        if iteration > 0:
            print(f"Iteration {iteration}, Best cost: {best_cost:.2f}")
        previous_best_cost = best_cost
        
        # Update pheromone matrix
        for i in range(n):
            for j in range(n):
                pheromone_matrix[i][j] = (1 - p) * pheromone_matrix[i][j]
                
        for tour, cost in zip(solutions, solution_costs):
            for i in range(n - 1):
                for j in range(i + 1, n):
                    pheromone_matrix[tour[i]][tour[j]] = pheromone_matrix[tour[i]][tour[j]] + q / cost
                    
        
    return best_cost, best_tour

if __name__ == '__main__':
    n, cost_matrix = read_input()
    best_cost, best_tour = ACO(n, cost_matrix)
    
    print(best_cost)
    print(' '.join(str(city) for city in best_tour))
    
    # Format the output
    # print(n)
    # print(" ".join(str(city + 1) for city in best_tour[:-1]))