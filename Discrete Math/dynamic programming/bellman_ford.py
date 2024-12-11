class Graph:
    def __init__(self, vertices):
        self.V = vertices
        self.edges = []
        
    def add_edge(self, u, v, weight):
        self.edges.append([u, v, weight])
        
    def bellman_ford(self, src):
        dist = [float('inf')] * self.V
        dist[src] = 0
        
        for _ in range(self.V - 1): # Relax all edges V - 1 times
            for u, v, weight in self.edges:
                if dist[u] != float('inf') and dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    
        return dist
    
    
g = Graph(7)

g.add_edge(0, 1, 6)
g.add_edge(0, 2, 5)
g.add_edge(0, 3, 5)
g.add_edge(1, 4, -1)
g.add_edge(2, 1, -2)
g.add_edge(2, 4, 1)
g.add_edge(3, 2, -2)
g.add_edge(3, 5, -1)
g.add_edge(4, 6, 3)
g.add_edge(5, 6, 3)

shortest_distances = g.bellman_ford(0)
if shortest_distances:
    print("Vertex Distance from Source")
    for i in range(len(shortest_distances)):
        print(f"{i}\t{shortest_distances[i]}")
