import random
import sys

def read_input():
    n = int(sys.stdin.readline().strip())
    cost_matrix = []
    for _ in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        cost_matrix.append(row)
    return n, cost_matrix 

def generate_initial_solution(size, num_cities):
    tour = [random.sample(range(num_cities), num_cities) for _ in range(size)]
    return tour

def calculate_fitness(chromosome, cost_matrix):
    total_cost = sum(cost_matrix[chromosome[i]][chromosome[i + 1]] for i in range(len(chromosome) - 1))
    total_cost = total_cost + cost_matrix[chromosome[-1]][chromosome[0]]
    fitness = 1 / total_cost
    return fitness

def select_parents(population, fitness_values):
    total_fitness = sum(fitness_values)
    probability_distribution = [f / total_fitness for f in fitness_values]
    parents = random.choices(
        population = population,
        weights = probability_distribution,
        k=2
    )
    return parents

def perform_crossover(parent1, parent2):
    size = len(parent1)
    start, end = sorted(random.sample(range(size), 2))
    offspring = [None] * size
    offspring[start : end + 1] = parent1[start : end + 1]
    remaining = [city for city in parent2 if city not in offspring]
    for i in range(size):
        if offspring[i] is None:
            offspring[i] = remaining.pop(0)
            
    return offspring

def perform_mutation(chromosome):
    i, j = random.sample(range(len(chromosome)), 2)
    chromosome[i], chromosome[j] = chromosome[j], chromosome[i]
    return chromosome

def create_new_population(population, offspring, elitism=True):
    if elitism:
        population = sorted(population, key=lambda x: x[1], reverse=True) # Sort by fitness in descending order
        population = population[:len(population) - len(offspring)]
        return population + offspring
    else:
        return offspring
    
    
def genetic_tsp(n, cost_matrix, population_size=100, generations=500, mutation_rate=0.25, elitism=True):
    population = generate_initial_solution(population_size, n)
    
    for generation in range(generations):
        fitness_values = [calculate_fitness(chromosome,cost_matrix) for chromosome in population]
        
        offspring = []
        for _ in range(len(population) // 2):
            parent1, parent2 = select_parents(population, fitness_values)
            child1 = perform_crossover(parent1, parent2)
            child2 = perform_crossover(parent2, parent1)
            
            if random.random() < mutation_rate:
                child1 = perform_mutation(child1)
                child2 = perform_mutation(child2)
            
            offspring.append(child1)
            offspring.append(child2)
            
        population = create_new_population(population, offspring, elitism)
    
    best_tour = max(population, key=lambda x: calculate_fitness(x, cost_matrix))
    best_cost = 1 / calculate_fitness(best_tour, cost_matrix)
    
    return best_tour, best_cost

if __name__ == "__main__":
    n, cost_matrix = read_input()
    
    best_tour, best_cost = genetic_tsp(n, cost_matrix)
    
    print(best_cost)
    print(' '.join(str(city) for city in best_tour))
    
            
            
                
                
            
        
    



















