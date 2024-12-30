import sys
import time
import random 

start_time = time.perf_counter()

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

# def generate_initial_solution(T, N, M, class_subjects, teacher_subjects, subject_hours, total_slots):
#     solution = []
#     assigned_slots = set()  # Track assigned (class, subject, teacher, slot)
#     for n in range(N):
#         for m in class_subjects[n]:
#             hours = subject_hours[m - 1]
#             teacher = random.choice([t for t in range(T) if m in teacher_subjects[t]])
#             start_slot = random.randint(0, total_slots - hours)
#             while (n, m, teacher, start_slot) in assigned_slots:  # Ensure uniqueness
#                 start_slot = random.randint(0, total_slots - hours)
#             solution.append((n, m, teacher, start_slot))
#             assigned_slots.add((n, m, teacher, start_slot))
#     return solution

def generate_initial_solution(T, N, M, class_subjects, teacher_subjects, subject_hours, total_slots):
    solution = []
    for n in range(N):
        for m in class_subjects[n]:
            hours = subject_hours[m - 1]
            teacher = random.randint(0, T - 1)  # Randomly assign any teacher
            start_slot = random.randint(0, total_slots - hours)  # Randomly assign a time slot
            solution.append((n, m, teacher, start_slot))
    return solution


def score_solution(solution, T, N, total_slots, subject_hours, teacher_subjects):
    score = 0
    penalties = 0
    
    class_schedule = [[False] * total_slots for _ in range(N)]
    teacher_schedule = [[False] * total_slots for _ in range(T)]
    
    for n, m, t, start_slot in solution:
        hours = subject_hours[m - 1] # 0-indexed
        for h in range(hours):
            slot = start_slot + h
            
            # Overlapping subjects for class
            if class_schedule[n][slot] == True:
                penalties += 2
            else:
                class_schedule[n][slot] = True
                
            # Overlapping assignments for a teacher 
            if teacher_schedule[t][slot] == True:
                penalties += 2
            else:
                teacher_schedule[t][slot] = True
                
        # Assigning to an unqualified teacher
        if m not in teacher_subjects[t]:
            penalties += 5
                
        score += 1
        
    return score - penalties 


# For a solution with L assignments, the total neighbours = L * ((L - 1) + (k - 1) + S) where k is the average number of qualified teachers per subject, S is the valid time slots for the subject  

def generate_neighbors(solution, T, total_slots, subject_hours, teacher_subjects):
    neighbors = set()  # Use a set to avoid duplicate neighbors
    for i, (n, m, t, start_slot) in enumerate(solution):
        hours = subject_hours[m - 1]

        # Swap two subjects
        for j in range(len(solution)):
            if i != j:
                new_solution = solution[:]
                new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
                neighbors.add(tuple(new_solution))

        # Reassign to a different teacher
        for new_teacher in range(T):
            if new_teacher != t and m in teacher_subjects[new_teacher]:
                new_solution = solution[:]
                new_solution[i] = (n, m, new_teacher, start_slot)
                neighbors.add(tuple(new_solution))

        # Move to a different time slot
        for new_start_slot in range(total_slots - hours):
            new_solution = solution[:]
            new_solution[i] = (n, m, t, new_start_slot)
            neighbors.add(tuple(new_solution))

    return [list(neighbor) for neighbor in neighbors]  # Convert back to list of solutions


def hill_climbing_timetable(T, N, M, class_subjects, teacher_subjects, subject_hours, D=5, S=12, max_iterations=100):
    total_slots = D * S

    current_solution = generate_initial_solution(T, N, M, class_subjects, teacher_subjects, subject_hours, total_slots)
    current_score = score_solution(current_solution, T, N, total_slots, subject_hours, teacher_subjects)

    # print(f"Initial Score: {current_score}")

    for iteration in range(max_iterations):
        neighbors = generate_neighbors(current_solution, T, total_slots, subject_hours, teacher_subjects)
        best_neighbor = max(neighbors, key=lambda sol: score_solution(sol, T, N, total_slots, subject_hours, teacher_subjects))
        best_score = score_solution(best_neighbor, T, N, total_slots, subject_hours, teacher_subjects)

        # print(f"Iteration {iteration + 1}, Best Score: {best_score}")

        if best_score > current_score:
            current_solution = best_neighbor
            current_score = best_score
        elif best_score == current_score:
            # Allow exploration of equally good neighbors to avoid early termination
            current_solution = best_neighbor
        else:
            break

    # Format output as per requirements
    formatted_output = []
    for n, m, t, start_slot in current_solution:
        period = start_slot + 1
        formatted_output.append((n + 1, m, period, t + 1))

    return formatted_output, current_score

if __name__ == "__main__":
    T, N, M, class_subjects, teacher_subjects, subject_hours = read_input()
    
    end_time = time.perf_counter()
    
    solution, score = hill_climbing_timetable(T, N, M, class_subjects, teacher_subjects, subject_hours)
    print(len(solution))
    for entry in solution:
        print(*entry)
    # print("Final Score:", score)
    # print("Time taken:", end_time - start_time)
