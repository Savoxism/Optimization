import sys
from ortools.sat.python import cp_model

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
        
    return m, n, A, B

def solve(m, n, A, B):
    model = cp_model.CpModel()
    
    teacher = [[0 for _ in range(m)] for _ in range(n)]
    
    # Decision variables 
    for i in range(n):  
        for j in range(m): 
            if i in A[j]:  
                teacher[i][j] = model.NewIntVar(0, 1, f"teacher_{i}_{j}")
            else:
                teacher[i][j] = model.NewIntVar(0, 0, f"teacher_{i}_{j}")
                
    # constraint 1: Each course is assigned to exactly one teacher.
    for i in range(n):
        model.Add(sum(teacher[i][j] for j in range(m)) == 1)
        
    # No two conflicting courses are assigned to the same teacher.
    for sub0, sub1 in B:
        for j in range(m):
            model.Add(teacher[sub0][j] + teacher[sub1][j] <= 1)
            
    z = model.NewIntVar(0, n, "z")
    for j in range(m):
        model.Add(z >= sum(teacher[i][j] for i in range(n)))
        
    model.Minimize(z)
            
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    # output
    if status == cp_model.OPTIMAL:
        print(int(solver.ObjectiveValue()))
    else:
        print("NO_SOLUTION")

if __name__ == "__main__":
    m, n, A, B = read_input()
    solve(m, n, A, B)