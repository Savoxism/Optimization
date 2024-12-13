#PYTHON 
from ortools.linear_solver import pywraplp
import sys

def input_data():
    m,n = [int(x) for x in input().split()]
    A = []
    for i in range(m):
        r = [int(x)-1 for x in input().split()[1:]]
        A.append(r)

    k = int(input())
    B = []
    for _ in range(k):
        [i,j] = [int(x)-1 for x in input().split()]
        B.append([i,j])
    
    return m,n,A,B

m,n,A, B = input_data()

solver = pywraplp.Solver.CreateSolver('SCIP')
INF = solver.infinity()

x = [[solver.IntVar(0,1,'x(' + str(t) + ',' + str(i) + ')' ) for i in range(n)] for t in range(n)]
y = [solver.IntVar(0, n, 'y(' + str(t) +')') for t in range (m)]
z = solver.IntVar(0, n, 'z')

for t in range(m):
    for i in range(n):
        if i not in A[t]:
            c = solver.Constraint(0,0)
            c.SetCoefficient(x[t][i],1)

for [i, j] in B:
    for t in range (m):
        c = solver.Constraint(0,1)
        c.SetCoefficient(x[t][i],1)
        c.SetCoefficient(x[t][j],1)

for t in range(m):
    c = solver.Constraint(0,0)
    for i in range(n):
        c.SetCoefficient(x[t][i],1)
    c.SetCoefficient(y[t],-1)

for t in range(m):
    c = solver.Constraint(0,INF)
    c.SetCoefficient(z,1)
    c.SetCoefficient(y[t],-1)

for i in range (n):
    c = solver.Constraint(1, 1)
    for t in range(m):
        c.SetCoefficient(x[t][i],1)

obj = solver.Objective()
obj.SetCoefficient(z,1)
# obj.SetMaximization()

status = solver.Solve()
print(int(solver.Objective().Value()))
