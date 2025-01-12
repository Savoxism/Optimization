from ortools.linear_solver import pywraplp
import sys

def read_input():
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

    
def cp_solve(m, n, A, B):
    solver = pywraplp.Solver.CreateSolver('SCIP')    
    INF = solver.infinity()
    
    x = [[solver.IntVar(0, 1, 'x(' + str(t) + ',' + str(i) + ')') for i in range(n)] for t in range(m)]
    y = [solver.IntVar(0, n, 'y(' + str(t) + ')') for t in range(m)]
    z = solver.IntVar(0, n, 'z')
    
    # constraint 1: teacher t can only teach courses that they are qualified
    for t in range(m):
        for i in range(n):
            if i not in A[t]:
                c = solver.Constraint(0, 0)
                c.SetCoefficient(x[t][i], 1)
                
    # constraint 2: conflicting courses cannot be assigned to the same teacher
    for [i, j] in B:
        for t in range(m):
            c = solver.Constraint(0, 1)
            c.SetCoefficient(x[t][i], 1)
            c.SetCoefficient(x[t][j], 1)
            
    # constraint 3: y[t] represents the number of courses assigned to teacher t
    for t in range(m):
        c = solver.Constraint(0, 0)
        for i in range(n):
            c.SetCoefficient(x[t][i], 1)
        c.SetCoefficient(y[t], -1)
        
    # constraint 4: z represents the number of teachers assigned to at least one course
    for t in range(m):
        c = solver.Constraint(0, INF)
        c.SetCoefficient(z, 1)
        c.SetCoefficient(y[t], -1)

        
    # constraint 5: each course is assigned to exactly one teacher
    for i in range(n):
        c = solver.Constraint(1, 1)
        for t in range(m):
            c.SetCoefficient(x[t][i], 1)
            
    objective_function = solver.Objective()
    objective_function.SetCoefficient(z, 1)
    
    solver.Solve()
    
    assignments = {t: [i for i in range(n) if x[t][i].solution_value() > 0.5] for t in range(m)}
    
    return int(solver.Objective().Value()), assignments

m, n, A, B = read_input()
value, assigments = cp_solve(m, n, A, B)

print(value)
print(assigments)