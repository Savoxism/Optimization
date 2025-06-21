import sys

'''
3 2
0 8 5 1 10 5 9
9 0 5 6 6 2 8
2 2 0 3 8 7 2
5 3 4 0 3 2 7
9 6 8 7 0 9 10
3 8 10 6 5 0 2
3 4 4 5 2 2 0
'''

n, k = map(int, sys.stdin.readline().split())
c = [list(map(int, sys.stdin.readline().split())) for _ in range(2 * n + 1)]

best = 9999999
visited = [False] * (2*n + 1)
load = 0

def backtrack(cur_pos, acc_cost, visited_count, load):
    global best
    
    if acc_cost > best:
        return
    
    # return to 0 
    if visited_count == 2 * n:
        best = min(best, acc_cost + c[cur_pos][0])
        
    for i in range(1, 2 * n + 1):
        if visited[i] == True:
            continue 
        
        if i <= n: # pick up
            if load < k: # bus has enough space
                visited[i] = True
                backtrack(i, acc_cost + c[cur_pos][i], visited_count + 1, load + 1)
                visited[i] = False
            
        elif n < i <= 2 * n: # drop-off (possible only if has been picked up)
            if visited[i - n]:
                visited[i] = True
                backtrack(i, acc_cost + c[cur_pos][i], visited_count + 1, load - 1)
                visited[i] = False

backtrack(0, 0, 0, 0)

print(best)
            
