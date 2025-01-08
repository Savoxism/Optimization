import random
import sys
import math

def read_input():
    n = int(sys.stdin.readline().strip())
    cost_matrix = []
    
    for _ in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        cost_matrix.append(row)
        
    return n, cost_matrix

def generate_initial_solution(n):
    initial_tour = list(range(n))
    random.shuffle(initial_tour)
    return initial_tour

def calculate_cost(tour, cost_matrix):
    total_cost = 0
    for i in range(len(tour)):
        total_cost += cost_matrix[tour[i]][tour[(i + 1) % len(tour)]]
    return total_cost

def generate_neighbor(tour):
    new_tour = tour[:]
    i, j = sorted(random.sample(range(len(tour)), 2))
    new_tour[i:j+1] = reversed(new_tour[i:j+1])
    return new_tour
    
def simulated_annealing():
    num_cities, cost_matrix = read_input()

    T0 = 1000
    alpha = 0.99
    min_temp = 1e-3
    max_iterations = 10000
    no_improvement_limit = 5000 
    
    # Initial solution
    current_tour = generate_initial_solution(num_cities)
    current_cost = calculate_cost(current_tour, cost_matrix)
    
    best_tour = current_tour[:]
    best_cost = current_cost
    
    T = T0
    iteration = 0
    no_improvement_counter = 0
    while T > min_temp and iteration < max_iterations:
        new_tour = generate_neighbor(best_tour)
        new_cost = calculate_cost(new_tour, cost_matrix)
        
        delta_E = new_cost - best_cost
        
        # condition 1: new tour yields lower cost
        # condition 2: new tour yields higher cost but satisfies Boltzmann condition
        if delta_E < 0 or random.random() < math.exp(-delta_E / T):
           current_tour = new_tour
           current_cost = new_cost
           
           if current_cost < best_cost:
               best_tour = current_tour
               best_cost = current_cost
               no_improvement_counter = 0
           else:
                no_improvement_counter = no_improvement_counter + 1
                
        if no_improvement_counter >= no_improvement_limit:
            print("Stopping early due to no improvement.")
            break
               
        T *= alpha
        iteration = iteration + 1
    
    return num_cities, best_cost, best_tour

# Example Usage
if __name__ == "__main__":
    num_cities, best_cost, best_tour = simulated_annealing()
    print(num_cities)
    print(" ".join(map(str, [x + 1 for x in best_tour])))  # Adding 1 to convert from 0-based to 1-based indexing