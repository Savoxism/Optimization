import sys
import time

start_total = time.perf_counter()
 
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

def assign_classes(T, N, M, class_subjects, teacher_subjects, subject_hours):
    SLOTS_PER_DAY = 12
    DAYS = 5
    total_slots = DAYS * SLOTS_PER_DAY

    # Each class/teacher schedule
    class_schedule = [[False] * total_slots for _ in range(N)] # Row: class, Column: slot, ensures that no two subjects for the same class overlap
    teacher_schedule = [[False] * total_slots for _ in range(T)] # Row: teacher, Column: slot, ensures that a teacher is not assigned to multiple classes at the same time

    # List of all class-subject combinations
    class_subject_combinations = []
    for c in range(N):
        for subject in class_subjects[c]:
            class_subject_combinations.append((c, subject))

    # Sort by subject hours descending (greedy criterion)
    class_subject_combinations.sort(key=lambda x: -subject_hours[x[1] - 1])

    # Result storage
    result = []

    for c, subject in class_subject_combinations:
        needed_hours = subject_hours[subject - 1] # 0-based index, the number of hours needed for this subject
        assigned = False

        for teacher in range(T):
            
            # Check whether the teacher is qualified to teach the subject
            if subject not in teacher_subjects[teacher]:
                continue
            
            # Try every possible starting time slot for the subject.
            for start_slot in range(total_slots - needed_hours + 1):
                # Ensure both the class and teacher are free for the required number of consecutive hours.
                if all(not class_schedule[c][start_slot + hour] for hour in range(needed_hours)) \
                    and all(not teacher_schedule[teacher][start_slot + h] for h in range(needed_hours)):

                    # Assign schedule
                    for hour in range(needed_hours):
                        class_schedule[c][start_slot + hour] = True
                        teacher_schedule[teacher][start_slot + hour] = True

                    # Convert the starting slot (start_slot) into a 1-based period.
                    period = start_slot + 1
                    result.append((c + 1, subject, period, teacher + 1))
                    
                    # Mark as assigned and break the loop
                    assigned = True
                    break 
                
            if assigned:
                break
            
    return result

def main():
    T, N, M, class_subjects, teacher_subjects, subject_hours = read_input()
    
    result = assign_classes(T, N, M, class_subjects, teacher_subjects, subject_hours)

    print(len(result))
    for r in result:
        print(*r)

if __name__ == "__main__":
    main()
