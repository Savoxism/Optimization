import sys
import numpy as np

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

def generate_solution(class_subjects, teacher_subjects, subject_hours, pheromone_matrix, T, N, M, alpha, beta):
    solution = []
    class_schedules = np.zeros((N, DAYS, SLOTS_PER_DAY), dtype=bool)
    teacher_schedules = np.zeros((T, DAYS, SLOTS_PER_DAY), dtype=bool)

    for n in range(N):
        for m in class_subjects[n]:
            duration = subject_hours[m - 1]
            available_teachers = [t for t in range(T) if m in teacher_subjects[t]]
            if not available_teachers:
                continue

            # Precompute heuristic values for all (teacher, day) pairs
            heuristic_matrix = np.zeros((T, DAYS))
            for t in available_teachers:
                for day in range(DAYS):
                    for s in range(SLOTS_PER_DAY - duration + 1):
                        if np.all(~teacher_schedules[t, day, s:s + duration]) and np.all(~class_schedules[n, day, s:s + duration]):
                            heuristic_matrix[t, day] = 1.0 / (s + 1)  # Prefer earlier slots
                            break
                    else:
                        heuristic_matrix[t, day] = 0.0  # No available slots

            # Compute probabilities for selecting (teacher, day) pairs
            probabilities = (pheromone_matrix ** alpha) * (heuristic_matrix ** beta)
            total_prob = np.sum(probabilities)

            # Skip if no valid (teacher, day) pairs are available
            if total_prob == 0:
                continue

            probabilities /= total_prob

            # Select a (teacher, day) pair based on probability
            selected_index = np.random.choice(T * DAYS, p=probabilities.flatten())
            selected_t, selected_day = np.unravel_index(selected_index, (T, DAYS))

            # Find the earliest available slot for the selected teacher and day
            for s in range(SLOTS_PER_DAY - duration + 1):
                if np.all(~teacher_schedules[selected_t, selected_day, s:s + duration]) and np.all(~class_schedules[n, selected_day, s:s + duration]):
                    teacher_schedules[selected_t, selected_day, s:s + duration] = True
                    class_schedules[n, selected_day, s:s + duration] = True
                    solution.append((n, m, selected_t, selected_day, s))
                    break

    return solution

def update_pheromone(pheromone_matrix, best_solution, evaporation_rate, rho=0.1):
    # Evaporate pheromone for all (teacher, day) pairs
    pheromone_matrix *= (1 - evaporation_rate)
    
    # Reinforce pheromone for assignments in the best solution
    for assignment in best_solution:
        t = assignment[2]  # Teacher
        d = assignment[3]  # Day
        pheromone_matrix[t, d] += rho

def ACO(T, N, M, class_subjects, teacher_subjects, subject_hours, num_ants=10, num_iterations=100, evaporation_rate=0.5, alpha=2.0, beta=1.0, rho=0.1):
    # Initialize pheromone matrix for (teacher, day) pairs
    pheromone_matrix = np.ones((T, DAYS), dtype=float)

    # Track the best solution found
    best_solution = []
    best_assignment_count = 0

    # Main loop
    for _ in range(num_iterations):
        # Each ant constructs a solution
        for ant in range(num_ants):
            solution = generate_solution(
                class_subjects, teacher_subjects, subject_hours, pheromone_matrix, T, N, M, alpha, beta
            )

            if len(solution) > best_assignment_count:
                best_solution = solution
                best_assignment_count = len(solution)

        update_pheromone(pheromone_matrix, best_solution, evaporation_rate, rho)

    return best_solution

if __name__ == "__main__":
    DAYS = 5
    SLOTS_PER_DAY = 12

    T, N, M, class_subjects, teacher_subjects, subject_hours = read_input()

    best_solution = ACO(T, N, M, class_subjects, teacher_subjects, subject_hours)

    final_assignments = []
    for assign in best_solution:
        n, m, t, d, s = assign
        final_assignments.append((n + 1, m, d * SLOTS_PER_DAY + s + 1, t + 1))

    # Output the results
    print(len(final_assignments))  # Total number of valid assignments
    for assign in final_assignments:
        print(assign[0], assign[1], assign[2], assign[3])