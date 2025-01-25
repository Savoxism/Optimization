import sys
from ortools.linear_solver import pywraplp

'''
2 3
30 20
12 17 20
2 3 1
1 2 5
'''
def read_input():
    lines = sys.stdin.readlines()
    
    n, m = map(int, lines[0].split())
    
    A = []
    for element in lines[1].split():
        A.append(int(element))
    
    B = []
    for element in lines[2].split():
        B.append(int(element))
        
    C = []
    for i in range(3, 3 + n):
        C.append(list(map(int, lines[i].split())))
        
    return n, m, A, B, C

def solve(n, m, A, B, C):
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    x = {}
    for i in range(n):
        for j in range(m):
            x[i, j] = solver.IntVar(0, solver.infinity(), f'x[{i},{j}]')
            
    # objective function
    objective = solver.Objective()
    for i in range(n):
        for j in range(m):
            objective.SetCoefficient(x[i, j], C[i][j])
    objective.SetMinimization()
    
    # supply constraint 
    for i in range(n):
        constraint = solver.Constraint(0, A[i])
        for j in range(m):
            constraint.SetCoefficient(x[i, j], 1)
            
    # demand constraint
    for j in range(m):
        constraint = solver.Constraint(B[j], solver.infinity()) 
        for i in range(n):
            constraint.SetCoefficient(x[i, j], 1)
            
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        K = 0
        results = []
        for i in range(n):
            for j in range(m):
                    K += 1
                    results.append((i + 1, j + 1, x[i, j].solution_value()))
        return K, results
    else:
        return None, None
    
n, m , A, B, C = read_input()
K, results = solve(n, m, A, B, C)
if K is not None:
    print(K)
    for result in results:
        print(result[0], result[1], result[2])
        