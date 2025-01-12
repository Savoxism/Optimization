import sys

'''
7 12 1 6
1 2 2 10
1 3 6 4
1 4 1 5
2 3 4 9
2 6 5 1
2 7 2 3
3 4 8 9
3 5 6 2
3 6 8 7
4 5 3 5
5 6 1 4
6 7 4 5
'''
def read_input():
    input = sys.stdin.read().splitlines()
    
    n, m, s, L = map(int, input[0].split())
    
    edges = []
    for line in input[1:]:
        u, v, t, c = map(int, line.split())
        edges.append((u, v, t, c))
        
    return n, m, s, L, edges

def solve(n, m, s, L, edges):
    # init adjacency list
    adj = [[] for _ in range(n+1)]
    for u, v, t, c in edges:
        adj[u].append((v, t, c))
       
    INF = float('inf')
    time = [INF] * (n + 1)  # time[i] = total transmission time from s to i
    cost = [INF] * (n + 1)  # cost[i] = total transmission cost from s to i
    time[s] = 0
    cost[s] = 0
    
    visited = [False] * (n + 1)
    
    for _ in range(n):
        u = -1
        min_time = INF
        
        for i in range(1, n + 1):
            if not visited[i] and time[i] < min_time:
                min_time = time[i]
                u = i
                
        if u == -1:
            break
        
        visited[u] = True
        
        for v, t, c in adj[u]:
            if not visited[v] and time[u] + t <= L and cost[u] + c < cost[v]:
                time[v] = time[u] + t
                cost[v] = cost[u] + c
          
    # check if all nodes are reachable within the time limit      
    for i in range(1, n + 1):
        if time[i] > L:
            return "NO_SOLUTION"
        
    total_cost = sum(cost[1:])
    
    return total_cost
    
if __name__ == "__main__":
    n, m, s, L, edges = read_input()
    total_cost = solve(n, m, s, L, edges)    
    print(total_cost)