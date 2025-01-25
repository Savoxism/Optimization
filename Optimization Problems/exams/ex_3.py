import sys
import heapq

'''
5 6
1 2 3
1 3 4
2 3 5
2 4 2
3 4 6
4 5 1
1
2
4 5
'''

def read_input():
    input = sys.stdin.readlines()
    
    n, m = map(int, input[0].split())
    
    edges = []
    for i in range(1, m + 1):
        u, v, w = map(int, input[i].split())
        edges.append((u, v, w))
    
    s = int(input[m + 1])
    K = int(input[m + 2])
    terminals = list(map(int, input[m + 3].split()))
    
    return n, m, edges, s, K, terminals

def dijsktra(n, adj, s):
    INF = float('inf')
    dist = [INF] * (n + 1)
    dist[s] = 0
    heap = [(0, s)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in adj[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(heap, (dist[v], v))
    return dist


######################
n, m, edges, s, K, terminals = read_input()

adj = [[] for _ in range(n + 1)]
for u, v, w in edges:
    adj[u].append((v, w))
    adj[v].append((u, w))

# Compute shortest paths from s to all terminals
dist = dijsktra(n, adj, s)
                
G = set() 
for t in terminals:
    current = t
    while current != s:
        for v, w in adj[current]:
            if dist[current] == dist[v] + w:
                G.add((v, current, w)) 
                current = v
                break
    
# Output the result
print(len(G))  
for u, v, w in G:
    print(u, v) 

