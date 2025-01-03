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

def generate_initial_solution_heuristic(T, N, M, class_subjects, teacher_subjects, subject_hours, DAYS, SLOTS_PER_DAY):
    class_schedules = {n: {day: set() for day in range(DAYS)} for n in range(N)}
    teacher_schedules = {t: {day: set() for day in range(DAYS)} for t in range(T)}
    solution = []
    
    for n in range(N):
        # Sort subjects by descending duration
        subjects = class_subjects[n]
        subjects_sorted = sorted(subjects, key=lambda m: -subject_hours[m - 1])
        
        for m in subjects_sorted:
            duration = subject_hours[m - 1]
            available_teachers = [t for t in range(T) if m in teacher_subjects[t]]
            
            # Sort teachers by their availability, preferring those who are less busy
            available_teachers_sorted = sorted(available_teachers, key=lambda t: sum(len(teacher_schedules[t][day]) for day in range(DAYS)))
            
            for t in available_teachers_sorted:
                # Find the earliest possible slot for this teacher and class
                for d in range(DAYS):
                    for s in range(SLOTS_PER_DAY - duration + 1):
                        if all(slot not in class_schedules[n][d] and slot not in teacher_schedules[t][d] for slot in range(s, s + duration)):
                            # Assign the subject to this time slot
                            for slot in range(s, s + duration):
                                class_schedules[n][d].add(slot)
                                teacher_schedules[t][d].add(slot)
                            solution.append((n, m, t, d, s))
                            break
                    else:
                        continue
                    break
                else:
                    continue
                break
            else:
                continue
    
    return solution

def evaluate_solution(solution, subject_hours):
    class_schedule = {}
    teacher_schedule = {}
    penalty = 0
    
    for assignment in solution:
        n, m, t, d, s = assignment
        duration = subject_hours[m - 1]
        
        # Check class overlap
        if n not in class_schedule:
            class_schedule[n] = set()
        for slot in range(s, s + duration):
            if (d, slot) in class_schedule[n]:
                penalty += 1  
            else:
                class_schedule[n].add((d, slot))
        
        # Check teacher overlap
        if t not in teacher_schedule:
            teacher_schedule[t] = set()
        for slot in range(s, s + duration):
            if (d, slot) in teacher_schedule[t]:
                penalty += 1
            else:
                teacher_schedule[t].add((d, slot))
                
    # Add a small penalty for higher 'u' values
    for assignment in solution:
        _, _, _, d, s = assignment
        u = d * SLOTS_PER_DAY + s + 1
        penalty += u * 0.01  
    return penalty

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
        # Change day and starting slot, preferring earlier days and slots
        d_new = random.randint(0, d)
        s_new = random.randint(0, s)
        neighbor[index] = (n, m, t, d_new, s_new)
    
    return neighbor

def SA(T, N, M, class_subjects, teacher_subjects, subject_hours, initial_temp, cooling_rate, min_temp, max_iterations):
    current_solution = generate_initial_solution_heuristic(T, N, M, class_subjects, teacher_subjects, subject_hours, DAYS, SLOTS_PER_DAY)
    current_penalty = evaluate_solution(current_solution, subject_hours)
    
    best_solution = current_solution
    best_penalty = current_penalty
    
    temperature = initial_temp
    iteration = 0
    
    while temperature > min_temp and iteration < max_iterations:
        iteration += 1
        
        neighbor = generate_neighbor(current_solution, T, N, M, class_subjects, teacher_subjects, subject_hours)
        neighbor_penalty = evaluate_solution(neighbor, subject_hours)
        
        delta_E = neighbor_penalty - current_penalty
        
        # Accept the new solution with a probability based on the penalty difference and temperature
        if delta_E < 0 or random.random() < math.exp(-delta_E / temperature):
            current_solution = neighbor
            current_penalty = neighbor_penalty
            
            if current_penalty < best_penalty:
                best_solution = current_solution
                best_penalty = current_penalty
                
        temperature *= cooling_rate
    
    return best_solution, best_penalty

def assignment(best_solution):
    class_schedule = {}
    teacher_schedule = {}
    valid_assignments = []
    for assignment in best_solution:
        n, m, t, d, s = assignment
        duration = subject_hours[m - 1]
        overlap_class = False
        overlap_teacher = False
        
        for slot in range(s, s + duration):
            if (d, slot) in class_schedule.get(n, set()):
                overlap_class = True
            if (d, slot) in teacher_schedule.get(t, set()):
                overlap_teacher = True
                
        if not overlap_class and not overlap_teacher:
            if n not in class_schedule:
                class_schedule[n] = set()
            if t not in teacher_schedule:
                teacher_schedule[t] = set()
            for slot in range(s, s + duration):
                class_schedule[n].add((d, slot))
                teacher_schedule[t].add((d, slot))
            valid_assignments.append(assignment)
    return valid_assignments


if __name__ == "__main__":
    T, N, M, class_subjects, teacher_subjects, subject_hours = read_input()
    initial_temp = 1000
    cooling_rate = 0.95
    min_temp = 1
    max_iterations = 100000  # Increased iterations
    
    best_solution, _ = SA(T, N, M, class_subjects, teacher_subjects, subject_hours, initial_temp, cooling_rate, min_temp, max_iterations)
        
    valid_assignments = assignment(best_solution)
    
    print(len(valid_assignments))  # K: Total number of valid assignments
    for assignment in valid_assignments:
        n, m, t, d, s = assignment
        # Convert to 1-based indexing for output
        x = n + 1  # Class ID
        y = m      # Subject ID
        u = d * SLOTS_PER_DAY + s + 1  # Starting time slot (1-based)
        v = t + 1  # Teacher ID
        print(x, y, u, v)
        
    # end_time = time.perf_counter()
    # print(f"Time: {end_time - start_time}")