# PYTHON
from ortools.linear_solver import pywraplp
import sys 

"""
4 12
5 1 3 5 10 12
5 9 3 4 8 12
6 1 2 3 4 9 7
7 1 2 3 5 6 10 11
25
1 2
1 3
1 5
2 4
2 5
2 6
3 5
3 7
3 10
4 6
4 9
5 6
5 7
5 8
6 8
6 9
7 8
7 10
7 11
8 9
8 11
8 12
9 12
10 11
11 12
"""

def read_input():
    input = sys.stdin.read().splitlines()
    
    # m: teachers, n: courses
    m, n = map(int, input[0].split())
    
    # Preference list
    A = []
    for i in range(1, m + 1):
        line = list(map(int, input[i].split()))
        courses = [x - 1 for x in line[1:]]  
        A.append(courses)
    
    # Number of conflicts
    k = int(input[m + 1])
    
    # Conflict pairs
    B = []
    for i in range(m + 2, m + 2 + k):
        u, v = map(int, input[i].split())
        B.append([u - 1, v - 1])  
        
    return m, n, A, B # m: teachers, n: courses, A: preference list , B: conflict pairs

def solve(m, n, A, B):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    inf = solver.infinity()
    
    # Decision variables
    x = [[solver.IntVar(0, 1, f"x_{i}_{j}") for j in range(n)] for i in range(m)]
            
    # each course is assigned to exactly one teacher
    for j in range(n):
            solver.Add(sum(x[i][j] for i in range(m)) == 1)
            
    # conflicting pairs cannot be assigned to the same teacher
    for sub1, sub2 in B:
        for i in range(m):
            solver.Add(x[i][sub1] + x[i][sub2] <= 1)
            
    # objective function
    z = solver.NumVar(lb=0, ub=inf, name="z")
    
    for i in range(m):
        solver.Add(z >= sum(x[i][j] for j in range(n)))
        
    solver.Minimize(z)
    # Solve the model
    status = solver.Solve()
    
    # Output the result
    if status == pywraplp.Solver.OPTIMAL:
        return int(solver.Objective().Value())
    else:
        return "NO_SOLUTION"
    
m, n, A, B = read_input()
result = solve(m, n, A, B)
print(result)
    
            
    
    
    
    
    
    
    
    
    