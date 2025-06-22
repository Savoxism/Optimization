import sys
import heapq

'''
n: nodes
m: edges
s: source
t: destination
Adj: adjacency matrix
'''

INF = int(1e9)

def input_data():
    n, m = map(int, sys.stdin.readline().split())
    Adj = [[] for _ in range(n + 1)]
    for _ in range(m):
        u, v, w = map(int, sys.stdin.readline().split())
        Adj[u].append((v, w))
    s, t = map(int, sys.stdin.readline().split())
    return n, m, Adj, s, t

def dijkstra(n, Adj, s, t):
    d = [INF] * (n + 1)
    found = [False] * (n + 1)
    pq = [(0, s)]  # (distance, node)

    while pq:
        dist_u, u = heapq.heappop(pq) # take the node with the smallest distance

        if u == t:
            return dist_u
        
        if dist_u > d[u]:
            continue

        for v, weight in Adj[u]:
            if d[v] > dist_u + weight:
                d[v] = dist_u + weight
                heapq.heappush(pq, (d[v], v))
    return -1


n, m, Adj, s, t = input_data()
result = dijkstra(n, Adj, s, t)
print(result)