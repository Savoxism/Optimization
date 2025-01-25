from ortools.sat.python import cp_model
import sys
import time

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

def solve():
    T, N, M, class_subjects, teacher_subjects, subject_hours = read_input()

    D = 5
    S = 12

    model = cp_model.CpModel()

    # Decision variables
    x = {}
    for n in range(N):
        for m in range(M):
            for t in range(T):
                for d in range(D):
                    for s in range(S):
                        x[n, m, t, d, s] = model.NewBoolVar(f"x[{n}][{m}][{t}][{d}][{s}]")

    # Constraints

    # 1. Each subject for a class must be taught for its required number of periods
    for n in range(N):
        for m in range(M):
            if m + 1 in class_subjects[n]:
                model.Add(
                    sum(x[n, m, t, d, s] for t in range(T) for d in range(D) for s in range(S)) == subject_hours[m]
                )

    # 2. A teacher can only teach one subject per period
    for t in range(T):
        for d in range(D):
            for s in range(S):
                model.Add(
                    sum(x[n, m, t, d, s] for n in range(N) for m in range(M)) <= 1
                )

    # 3. A class can only have one subject per period
    for n in range(N):
        for d in range(D):
            for s in range(S):
                model.Add(
                    sum(x[n, m, t, d, s] for m in range(M) for t in range(T)) <= 1
                )

    # 4. Teachers must not teach subjects they are not qualified for
    for t in range(T):
        for m in range(M):
            if m + 1 not in teacher_subjects[t]:
                for n in range(N):
                    for d in range(D):
                        for s in range(S):
                            model.Add(x[n, m, t, d, s] == 0)

    # Objective function: Maximize the total assignments
    model.Maximize(
        sum(x[n, m, t, d, s] for n in range(N) for m in range(M) for t in range(T) for d in range(D) for s in range(S))
    )

    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)

    # Output the solution
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        result = []
        for n in range(N):
            for m in range(M):
                if m + 1 in class_subjects[n]:
                    assigned = False
                    for t in range(T):
                        for d in range(D):
                            for s in range(S):
                                if solver.Value(x[n, m, t, d, s]) == 1:
                                    if not assigned:
                                        # First assignment for the subject
                                        start_period = d * S + s + 1
                                        result.append((n + 1, m + 1, start_period, t + 1))
                                        assigned = True

        # Print the results in the specified format
        print(len(result))
        for entry in result:
            print(*entry)
    else:
        print(0)

if __name__ == "__main__":
    solve()
    
    # end_time = time.perf_counter()
    
    # print(f"Time taken: {end_time - start_time} seconds")
