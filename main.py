import random

def initialize_population(num_courses, num_teachers, population_size):
    """Initialize population with random valid assignments."""
    return [
        [random.randint(0, num_teachers - 1) for _ in range(num_courses)]
        for _ in range(population_size)
    ]

# Test the function
num_courses = 5  # Number of courses
num_teachers = 3  # Number of teachers
population_size = 10  # Population size

# Generate the population
population = initialize_population(num_courses, num_teachers, population_size)
print(population)
