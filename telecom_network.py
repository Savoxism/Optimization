import sys

def read_input():
    input = sys.stdin.read().split()
    idx = 0
    n = int(input[idx])
    m = int(input[idx + 1])
    idx += 2
    
    graph = {i: {} for i in range(1, n + 1)}
    
    for _ in range(m):
        u = int(input[idx])
        v = int(input[idx + 1])
        w = int(input[idx + 2])
        
        graph[u][v] = w
        graph[v][u] = w
        idx += 3
        
    s = int(input[idx])   
    idx += 1
    
    K = int(input[idx])
    idx += 1
    
    T = list(map(int, input[idx:idx+K]))
    idx += K
    
    return n, m, graph, s, T

def dijkstra(graph, source):
    # Initialize distances to all nodes as infinity
    distances = {node: float('inf') for node in graph}
    
    distances[source] = 0
    visited = set()
    
    while True:
        current_node = None
        min_distance = float('inf')
        
        # Find the closest unvisited node 
        for node in graph:
            if node not in visited and distances[node] < min_distance:
                current_node = node
                min_distance = distances[node]
        
        # If all nodes have been visited
        if current_node is None:
            break
        
        visited.add(current_node)
        
        # Choosing the minimum distance node
        for neighbor, weight in graph[current_node].items():
            distance = distances[current_node] + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                
    return distances

if __name__ == "__main__":
    n, m, graph, s, T = read_input()
    
    distances = dijkstra(graph, s)
    
    edges = set()
    for t in T:
        current = t
        while current != s:
            for neighbor, weight in graph[current].items():
                if distances[neighbor] + weight == distances[current]:
                    edges.add((min(current, neighbor), max(current, neighbor)))
                    current = neighbor
                    break
    
    print(len(edges))
    
    for edge in sorted(edges):
        print(edge[0], edge[1])
        
