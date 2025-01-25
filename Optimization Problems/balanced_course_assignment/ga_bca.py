import random
import sys

def input_data():
    # Read the first line for the number of teachers (m) and courses (n)
    m, n = map(int, sys.stdin.readline().strip().split())
    
    # Read the next m lines for the preference list
    A = []
    for _ in range(m):
        line = list(map(int, sys.stdin.readline().strip().split()))
        courses = [x - 1 for x in line[1:]]  # Skip the first number (k) and convert to zero-based indexing
        A.append(courses)
    
    # Read the number of conflicts
    k = int(sys.stdin.readline().strip())
    
    # Read the next k lines for the conflict pairs
    B = []
    for _ in range(k):
        i, j = map(int, sys.stdin.readline().strip().split())
        B.append([i - 1, j - 1])  # Convert to zero-based indexing
    
    return m, n, A, B

def initialize_population(num_courses, num_teachers, population_size):
    """Initialize population ensuring each course is assigned to exactly one teacher."""
    population = []
    for _ in range(population_size):
        assignment = {t: [] for t in range(num_teachers)}
        for course in range(num_courses):
            teacher = random.randint(0, num_teachers - 1)
            assignment[teacher].append(course)
        population.append(assignment)
    return [{t: sorted(assignment[t]) for t in assignment} for assignment in population]


def calculate_fitness(individual, num_teachers, preferences, conflicts):
    """Calculate fitness based on maximum load and constraint violations."""
    loads = [len(individual[t]) for t in range(num_teachers)]
    max_load = max(loads)

    penalty = 0

    # Penalize courses assigned to teachers who are not qualified
    for teacher, courses in individual.items():
        for course in courses:
            if course not in preferences[teacher]:
                penalty += 10

    # Penalize conflicting courses assigned to the same teacher
    for teacher, courses in individual.items():
        for i in range(len(courses)):
            for j in range(i + 1, len(courses)):
                if [courses[i], courses[j]] in conflicts or [courses[j], courses[i]] in conflicts:
                    penalty += 10

    # Penalize duplicate course assignments
    all_courses = [course for courses in individual.values() for course in courses]
    if len(all_courses) != len(set(all_courses)):
        penalty += 50  # Large penalty for duplicate course assignments

    return max_load + penalty

            
def tournament_selection(population, fitness_scores, k=3):
    selected = random.sample(list(zip(population, fitness_scores)), k)
    return min(selected, key=lambda x: x[1])[0]

def crossover(parent1, parent2):
    """Perform single-point crossover ensuring no duplicate assignments."""
    point = random.randint(0, len(parent1) - 1)
    child1 = {t: [] for t in parent1}
    child2 = {t: [] for t in parent1}

    for teacher in parent1:
        if teacher <= point:
            child1[teacher] = parent1[teacher]
            child2[teacher] = parent2[teacher]
        else:
            child1[teacher] = parent2[teacher]
            child2[teacher] = parent1[teacher]

    # Reassign duplicate courses
    for child in [child1, child2]:
        all_courses = [course for courses in child.values() for course in courses]
        duplicates = [course for course in all_courses if all_courses.count(course) > 1]
        available_teachers = list(child.keys())

        for course in duplicates:
            for teacher, courses in child.items():
                if course in courses:
                    courses.remove(course)
                    break
            new_teacher = random.choice(available_teachers)
            child[new_teacher].append(course)

    return child1, child2


def mutate(individual, num_teachers, mutation_rate):
    """Introduce random changes to an individual while maintaining valid assignments."""
    all_courses = [course for courses in individual.values() for course in courses]
    for teacher, courses in individual.items():
        for i in range(len(courses)):
            if random.random() < mutation_rate:
                new_teacher = random.randint(0, num_teachers - 1)
                if new_teacher != teacher:
                    course = courses.pop(i)
                    individual[new_teacher].append(course)

    # Ensure no duplicate courses
    duplicates = [course for course in all_courses if all_courses.count(course) > 1]
    for course in duplicates:
        for teacher, courses in individual.items():
            if course in courses:
                courses.remove(course)
                break
        new_teacher = random.randint(0, num_teachers - 1)
        individual[new_teacher].append(course)

    return individual


def genetic_algorithm(num_courses, num_teachers, preferences, conflicts, population_size=100, generations=1000, mutation_rate=0.1):
    population = initialize_population(num_courses, num_teachers, population_size)
    
    for generation in range(generations):
        fitness_scores = [calculate_fitness(individual, num_teachers, preferences, conflicts) for individual in population]
        
        # Find the best solution
        best_individual = population[fitness_scores.index(min(fitness_scores))]
        best_fitness = min(fitness_scores)

        # Early stopping if perfect solution is found
        if best_fitness == min(fitness_scores):
            break
        
        new_population = []
        
        # Generate new population
        for _ in range(population_size // 2):
            parent1 = tournament_selection(population, fitness_scores)
            parent2 = tournament_selection(population, fitness_scores)
            child1, child2 = crossover(parent1, parent2)
            mutate(child1, num_teachers, mutation_rate)
            mutate(child2, num_teachers, mutation_rate)
            new_population.extend([child1, child2])

        population = new_population

    return best_individual, best_fitness

m, n, A, B = input_data()
best_solution, best_fitness = genetic_algorithm(n, m, A, B)

# Print results in the required format
print(best_fitness)
for teacher, courses in best_solution.items():
    print(teacher + 1, *[(course + 1) for course in sorted(courses)])
