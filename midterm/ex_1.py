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
    input = sys.stdin.read()
    lines = input.split('\n')
    
    n, m  = map(int, lines[0].split())
    A = list(map(int, lines[1].split()))
    B = list(map(int, lines[2].split()))    
    C = []
    for i in range(n):
        C.append(list(map(int, lines[3+i].split())))
                 
    return n, m, A, B, C

def solve(n, m, A, B, C): 
    solver = pywraplp.Solver.CreateSolver('GLOP')
    
    x = [
        [solver.NumVar(0, solver.infinity(), f'x[{i}][{j}]') for j in range(m)] for i in range(n)
        ]
    
    for i in range(n):
        solver.Add(solver.Sum(x[i][j] for j in range(m)) <= A[i])
        
    for j in range(m):
        solver.Add(solver.Sum(x[i][j] for i in range(n)) >= B[j])
        
    # objective function
    solver.Minimize(solver.Sum(C[i][j] * x[i][j] for i in range(n) for j in range(m)))
    
    status = solver.Solve()
    
    if status == pywraplp.Solver.OPTIMAL:
        allocations = []
        for i in range(n):
            for j in range(m):
                allocations.append((i + 1, j + 1, float(x[i][j].solution_value())))  

        return len(allocations), allocations
    else:
        return "NOT_FEASIBLE"
    
n, m, A, B, C = read_input()

K, solution = solve(n, m, A, B, C)

print(K)

for i, j, g in solution:
    print(i, j, g)