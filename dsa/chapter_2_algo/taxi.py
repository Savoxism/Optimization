#PYTHON 
import sys
sys.setrecursionlimit(10**7) 

'''
2
0 8 5 1 10
5 0 9 3 5
6 6 0 8 2
2 6 3 0 7
2 5 3 4 0
'''

input = sys.stdin.readline
n = int(input())

# (2n+1) * (2n+1) distance matrix
c = [list(map(int, input().split())) for _ in range(2*n+1)]

best = 999999
used = [False] * (n + 1)

def dfs(served, last_position, accumulated_cost):
    global best
    # prunning
    if accumulated_cost > best:
        return
    
    if served == n:
        total = accumulated_cost + c[last_position][0]
        if total < best:
            best = total
        return 
    
    # try with each unserved passenger i 
    for i in range(1, n + 1):
        if not used[i]:
            used[i]=True
            
            step_cost = c[last_position][i] + c[i][i+n]
            dfs(served + 1, i + n, accumulated_cost + step_cost)
            
            used[i] = False
        
dfs(0, 0, 0)

print(best)
