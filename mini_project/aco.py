import sys
import random

# Constants
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

def is_time_slot_available(schedule, day, start_slot, duration):
    # Check if the required number of slots exceeds the remaining slots in the day
    if start_slot + duration > SLOTS_PER_DAY:
        return False
    
    # Check if all required slots are free
    for slot in range(start_slot, start_slot + duration):
        if schedule[day][slot]:  
            return False
        
    return True

def assign_time_slots(schedule, day, start_slot, duration):
    for slot in range(start_slot, start_slot + duration):
        schedule[day][slot] = True

def unassign_time_slots(schedule, day, start_slot, duration):
    for slot in range(start_slot, start_slot + duration):
        schedule[day][slot] = False
        
def find_earliest_available_slot(class_schedule, teacher_schedule, day, duration):
    for s in range(SLOTS_PER_DAY - duration + 1):
        if is_time_slot_available(class_schedule, day, s, duration) and is_time_slot_available(teacher_schedule, day, s, duration):
            return s
    return None

def heuristic_value(teacher_schedule, day, duration):
    for s in range(SLOTS_PER_DAY - duration + 1):
        if is_time_slot_available(teacher_schedule, day, s, duration):
            return 1.0 / (s + 1)
    return 0.0

def ant_construct_schedule(class_subjects, teacher_subjects, subject_hours, pheromone, class_schedules, teacher_schedules, T, N, M, DAYS, SLOTS_PER_DAY, alpha, beta):
    schedule = []
    for n in range(N):
        for m in class_subjects[n]:
            duration = subject_hours[m-1]
            eligible_teachers = [t for t in range(T) if m in teacher_subjects[t]]
            if not eligible_teachers:
                continue
            # Calculate denominator for probability
            denominator = sum(
                (pheromone[(t, day)] ** alpha) * (heuristic_value(teacher_schedules[t], day, duration) ** beta)
                for t in eligible_teachers
                for day in range(DAYS)
            )
            if denominator == 0:
                continue
            # Select a teacher and day based on probability
            r = random.uniform(0, denominator)
            cumulative = 0.0
            selected_t = None
            selected_day = None
            for t in eligible_teachers:
                for day in range(DAYS):
                    prob = (pheromone[(t, day)] ** alpha) * (heuristic_value(teacher_schedules[t], day, duration) ** beta)
                    cumulative += prob
                    if cumulative >= r:
                        selected_t = t
                        selected_day = day
                        break
                else:
                    continue
                break
            else:
                continue
            # Find the earliest available slot for the selected teacher and day
            s = find_earliest_available_slot(class_schedules[n], teacher_schedules[selected_t], selected_day, duration)
            if s is not None:
                assign_time_slots(class_schedules[n], selected_day, s, duration)
                assign_time_slots(teacher_schedules[selected_t], selected_day, s, duration)
                schedule.append((n, m, selected_t, selected_day, s, duration))
    return schedule

def update_pheromone(pheromone, best_schedule, evaporation_rate, rho=0.1):
    """
    Update pheromone levels based on the best schedule found.
    """
    # Evaporate pheromone for all (teacher, day) pairs
    for key in pheromone:
        pheromone[key] *= (1 - evaporation_rate)
    
    # Reinforce pheromone for assignments in the best schedule
    for assignment in best_schedule:
        t = assignment[2]  # Teacher
        d = assignment[3]  # Day
        pheromone[(t, d)] += rho
        
def aco_scheduling(T, N, M, class_subjects, teacher_subjects, subject_hours, num_ants=10, num_iterations=100, evaporation_rate=0.5, alpha=1.0, beta=2.0, rho=0.1):
    class_schedules = {n: {d: [False]*SLOTS_PER_DAY for d in range(DAYS)} for n in range(N)}
    teacher_schedules = {t: {d: [False]*SLOTS_PER_DAY for d in range(DAYS)} for t in range(T)}
    pheromone = { (t, d): 1.0 for t in range(T) for d in range(DAYS) }
    best_schedule = []
    best_assignment_count = 0
    for iteration in range(num_iterations):
        ant_class_schedules = {n: {d: [False]*SLOTS_PER_DAY for d in range(DAYS)} for n in range(N)}
        ant_teacher_schedules = {t: {d: [False]*SLOTS_PER_DAY for d in range(DAYS)} for t in range(T)}
        for ant in range(num_ants):
            schedule = ant_construct_schedule(class_subjects, teacher_subjects, subject_hours, pheromone, ant_class_schedules, ant_teacher_schedules, T, N, M, DAYS, SLOTS_PER_DAY, alpha, beta)
            if len(schedule) > best_assignment_count:
                best_schedule = schedule
                best_assignment_count = len(schedule)
        update_pheromone(pheromone, best_schedule, evaporation_rate, rho)
    final_assignments = []
    for assign in best_schedule:
        n, m, t, d, s, duration = assign
        x = n + 1
        y = m
        u = d * SLOTS_PER_DAY + s + 1
        v = t + 1
        final_assignments.append((x, y, u, v))
    print(len(final_assignments))
    for assign in final_assignments:
        print(assign[0], assign[1], assign[2], assign[3])
        
if __name__ == "__main__":
    T, N, M, class_subjects, teacher_subjects, subject_hours = read_input()
    aco_scheduling(T, N, M, class_subjects, teacher_subjects, subject_hours)