from ortools.linear_solver import pywraplp
import time 

start_total = time.perf_counter()

def Input():
    [T, N, M] = [int(x) for x in input().split()]
    course_for_class = []
    
    for _ in range(N):
        row = [int(x) - 1 for x in input().split()] #the subject is start at 0
        course_for_class.append(row[:-1])
    preference = []
    
    for _ in range(T):
        row = [int(x) - 1 for x in input().split()] #the subject is start at 0
        preference.append(row)
    load = [int(x) for x in input().split()]
    return T, N, M, course_for_class, preference, load

T, N, M, course_for_class, preference, load = Input()

# the upper bound of the objective
objective_max_val = 0
for subjects in course_for_class:
    objective_max_val += len(subjects)
    
# the subject can be taught by these teacher
teachable = [[] for _ in range(M)]
for s in range(M):
    for t in range(T):
        if s in preference[t]:
            teachable[s].append(t)
# print(teachable)

# create solver
solver = pywraplp.Solver.CreateSolver("GLOP")
        
# decision variables (class, subject, teacher, period, timeslot)
x = {}
# class, subject
y = {}
# if create only for the pair c-s in course for class,
# if create only for the c-s-t available in teachable
# the search speace is smaller

for c in range(N):
    for s in course_for_class[c]:
        for t in teachable[s]:
            for p in range(10): #10 periods
                for ts in range(6):  # 6 time slots per period
                    x[c, s, t, p, ts] = solver.BoolVar(f'x[{c},{s},{t},{p},{ts}]')
        y[c, s] = solver.BoolVar(f'y[{c},{s}]')
        
Objective = solver.IntVar(0,objective_max_val,'Objective')


## Constraints from here
for c in range(N):
    for s in course_for_class[c]:
        solver.Add(solver.Sum(x[c,s,t,p,ts]
                              for t in teachable[s]
                              for p in range(10)
                              for ts in range(6)) <= 1)
        
        solver.Add(y[c,s] == sum(x[c,s,t,p,ts] 
                                 for t in teachable[s]
                                 for p in range(10)
                                 for ts in range(6))) 

# class schedule non-overlap
for c in range(N):
    for p in range(10):
        for ts in range(6):
            solver.Add(solver.Sum(x[c,s,t,p,ts2]
                                  for s in course_for_class[c]
                                  for t in teachable[s]
                                  for ts2 in range(min(ts+load[s],6)) #adjusted the range
                                  ) <= 1)
            
# teacher schedule non-overlap
for t in range(T):
    for p in range(10):
        for ts in range(6):
            solver.Add(solver.Sum(x[c,s,t,p,ts2]
                                  for c in range(N)
                                  for s in course_for_class[c]
                                  for ts2 in range(min(ts+load[s],6)) #adjusted the range
                                  if t in teachable[s]
                                  ) <= 1)


# Objective: Maximize the number of assigned class-subject pairs
solver.Add(solver.Sum(y[c, s] for c in range(N) for s in course_for_class[c]) == Objective)
solver.Maximize(Objective)

status = solver.Solve()

if status == pywraplp.Solver.OPTIMAL:
    print(int(Objective.solution_value()))
    for c in range(N):
        for s in course_for_class[c]:
            for t in teachable[s]:
                for p in range(10):
                    for ts in range(6):
                        if x[c, s, t, p, ts].solution_value() == 1:
                            print(c + 1 , s + 1, p * 6 + ts + 1, t + 1)
else: 
    print(-1)
    
end_total = time.perf_counter()

print(f"Total Execution Time: {end_total - start_total:.2f} seconds")