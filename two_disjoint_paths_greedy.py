import sys

def read_input():
    input = sys.stdin.read().splitlines()
    n_m = input[0].split()
    n = int(n_m[0])
    m = int(n_m[1])
    
    graph = [[] for _ in range(n + 1)]
    for i in range(1, m + 1):
        u_v_c = input[i].split()
        u = int(u_v_c[0])
        v = int(u_v_c[1])
        c = int(u_v_c[2])
        graph[u].append((v, c))
        graph[v].append((u, c))
    
    return n, m, graph

def dijkstra(graph, n, start, end, removed_edges):
    INF = 10**9
    dist = [INF] * (n + 1) 
    dist[start] = 0
    
    visited = [False] * (n + 1)
    
    prev = [-1] * (n + 1) # To reconstruct the path
    
    for _ in range(n):
        # find the node with the smallest distance
        u = -1
        min_dist = INF
        
        for i in range(1, n + 1):
            if not visited[i] and dist[i] < min_dist:
                min_dist = dist[i]
                u = i
            
        # If all nodes are visited
        if u == -1:
            break
        
        visited[u] = True
        
        # Relax egdes
        for v, c in graph[u]:
            if (u, v) in removed_edges or (v, u) in removed_edges:
                continue
            
            dist_v = dist[u] + c
            if dist[v] > dist_v:
                dist[v] = dist_v
                prev[v] = u
                
    if dist[end] == INF:
        return None, None
    
    # Reconstruct the path
    path = []
    u = end
    while u != -1:
        path.append(u)
        u = prev[u]
    path.reverse()
    
    return dist[end], path

def solve(graph, n):
    dist1, path1 = dijkstra(graph, n, 1, n, set())
    if not path1:
        return "NOT_FEASIBLE"
    
    # Remove edges from the first path
    removed_edges = set()
    for i in range(len(path1) - 1):
        u = path1[i]
        v = path1[i + 1]
        removed_edges.add((u, v))
        
    dist2, path2 = dijkstra(graph, n, 1, n, removed_edges)
    if not path2:
        return "NOT_FEASIBLE"
    
    return dist1 + dist2

if __name__ == "__main__":
    n, m, graph = read_input()
    result = solve(graph, n)
    print(result)