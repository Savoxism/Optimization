import sys
import time
import random
import math

start_time = time.perf_counter()
DAYS = 5
SLOTS_PER_DAY = 12

def read_input():
    input = sys.stdin.read
    data = input().splitlines()
    
    T, N, M = map(int, data[0].split())
    
    class_subjects = []
    for i in range(1, N + 1): 
        class_subjects.append(list(map(int, data[i].split()))[:-1])

    teacher_subjects = []
    for i in range(N + 1, N + T + 1):
        teacher_subjects.append(list(map(int, data[i].split()))[:-1])

    subject_hours = list(map(int, data[N + T + 1].split()))

    return T, N, M, class_subjects, teacher_subjects, subject_hours

def generate_initial_solution(T, N, M, class_subjects, teacher_subjects, subject_hours):
    solution = []
    for n in range(N):
        for m in class_subjects[n]:
            available_teachers = [t for t in range(T) if m in teacher_subjects[t]]
            if not available_teachers:
                continue  
            t = random.choice(available_teachers)
            d = random.randint(0, DAYS - 1)
            s = random.randint(0, SLOTS_PER_DAY - subject_hours[m - 1])
            solution.append((n, m, t, d, s))
    return solution

# Returns the number of valid assignments in the solution, the higher the more quality of the solution 
def evaluate_solution(solution, subject_hours):
    class_schedule = {}
    teacher_schedule = {}
    
    for assignment in solution:
        n, m, t, d, s = assignment
        
        # Check class overlap
        if n not in class_schedule:
            class_schedule[n] = set()
        for slot in range(s, s + subject_hours[m - 1]):
            if (d, slot) in class_schedule[n]:
                return -1  
            class_schedule[n].add((d, slot))
            
        # Check teacher overlap
        if t not in teacher_schedule:
            teacher_schedule[t] = set()
        for slot in range(s, s + subject_hours[m - 1]):
            if (d, slot) in teacher_schedule[t]:
                return -1
            teacher_schedule[t].add((d, slot))
            
    return len(solution)

def generate_neighbor(solution, T, N, M, class_subjects, teacher_subjects, subject_hours):
    neighbor = solution.copy()
    index = random.randint(0, len(neighbor) - 1)
    n, m, t, d, s = neighbor[index]
    
    if random.random() < 0.5:
        # Change teacher
        available_teachers = [t for t in range(T) if m in teacher_subjects[t]]
        if available_teachers:
            t_new = random.choice(available_teachers)
            neighbor[index] = (n, m, t_new, d, s)
    else:
        # Change day and starting slot
        d_new = random.randint(0, DAYS - 1)
        s_new = random.randint(0, SLOTS_PER_DAY - subject_hours[m - 1])
        neighbor[index] = (n, m, t, d_new, s_new)
    
    return neighbor


def SA(T, N, M, class_subjects, teacher_subjects, subject_hours, initial_temp, cooling_rate, min_temp, max_iterations):
    
    current_solution = generate_initial_solution(T, N, M, class_subjects, teacher_subjects, subject_hours)
    current_value = evaluate_solution(current_solution, subject_hours)
    
    best_solution = current_solution
    best_value = current_value
    
    temperature = initial_temp
    iteration = 0
    
    while temperature > min_temp and iteration < max_iterations:
        iteration += 1
        
        neighbor = generate_neighbor(current_solution, T, N, M, class_subjects, teacher_subjects, subject_hours)
        neighbor_value = evaluate_solution(neighbor, subject_hours)
        
        if neighbor_value == -1:
            continue
        
        delta_E = neighbor_value - current_value
        
        # Accept the new solution if it is better or with a certain probability if it is worse
        if delta_E > 0 or random.random() < math.exp(delta_E / temperature):
            current_solution = neighbor
            current_value = neighbor_value
            
        # Update the best solution if necessary
        if current_value > best_value:
            best_solution = current_solution
            best_value = current_value
            
        temperature = temperature * cooling_rate
        
        # Print progress every 100 iterations
        if iteration % 100 == 0:
            print(f"Iteration: {iteration}, Temperature: {temperature:.2f}, Best Value: {best_value}")
    
    return best_solution, best_value

if __name__ == "__main__":
    T, N, M, class_subjects, teacher_subjects, subject_hours = read_input()
    initial_temp = 1000
    cooling_rate = 0.95
    min_temp = 1
    max_iterations = 50000
    
    best_solution, best_value = SA(T, N, M, class_subjects, teacher_subjects, subject_hours, initial_temp, cooling_rate, min_temp, max_iterations)

    # Output the results in the required format
    print(best_value)  # K: Total number of valid assignments
    for assignment in best_solution:
        n, m, t, d, s = assignment
        # Convert to 1-based indexing for output
        x = n + 1  # Class ID
        y = m      # Subject ID
        u = d * SLOTS_PER_DAY + s + 1  # Starting time slot (1-based)
        v = t + 1  # Teacher ID
        print(x, y, u, v)
        
    end_time = time.perf_counter()
    print(f"Time: {end_time - start_time}")