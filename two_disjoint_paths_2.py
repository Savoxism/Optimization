from ortools.sat.python import cp_model
import sys

def input():
    n,m = map(int,sys.stdin.readline().split())
    paths = []
    for i in range(m):
        b,a,c  = map(int,sys.stdin.readline().split())
        paths.append([b,a,c])
    return n,m,paths
n,m,paths = input()

model = cp_model.CpModel()

#create values
path1 = []
path2 = []
for index in range(m):
    path1.append(model.NewBoolVar("index"))
    path2.append(model.NewBoolVar("index"))

    model.Add(path1[index] + path2[index] <= 1)

for node in range(1,n+1):
    #exactly one edge start from node 1
    if node==1:
        model.Add(sum(path1[index] for index in range(m) if paths[index][0] == 1) == 1)
        model.Add(sum(path2[index] for index in range(m) if paths[index][0] == 1) == 1)
    #exactly one edge go to the end node
    elif node==n:
        model.Add(sum(path1[index] for index in range(m) if paths[index][1] == n) == 1)
        model.Add(sum(path2[index] for index in range(m) if paths[index][1] == n) == 1)
    #other nodes constraints
    else:
        model.Add(sum(path1[index] for index in range(m) if paths[index][0] == node) <= 1)
        model.Add(sum(path2[index] for index in range(m) if paths[index][0] == node) <= 1)
        model.Add(sum(path1[index] for index in range(m) if paths[index][1] == node) <= 1)
        model.Add(sum(path2[index] for index in range(m) if paths[index][1] == node) <= 1)
        model.Add(sum(path1[index] for index in range(m) if paths[index][0] == node) == sum(path1[index] for index in range(m) if paths[index][1] == node))
        model.Add(sum(path2[index] for index in range(m) if paths[index][0] == node) == sum(path2[index] for index in range(m) if paths[index][1] == node))
    
totalCost = sum(paths[index][2] * (path1[index]+path2[index]) for index in range(m))
model.Minimize(totalCost)

solver = cp_model.CpSolver()
status = solver.Solve(model)

if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
    print(int(solver.ObjectiveValue()))
else:
    print("NOT_FEASIBLE")