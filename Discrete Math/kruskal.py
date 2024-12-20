def kruskals_algorithm(graph):
    mst = []
    edges = []
    parent = {}
    rank = {}
    
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]
    
    def union(node1, node2):
        root1 = find(node1)
        root2 = find(node2)
        
        if root1 != root2:
            if rank[root1] > rank[root2]:
                parent[root2] = root1
            elif rank[root1] < rank[root2]:
                parent[root1] = root2
            else:
                parent[root2] = root1
                rank[root1] += 1
                
    # Initialize the edges list and union-find structure
    for node in graph:
        for neighbor, weight in graph[node]:
            edges.append((node, neighbor, weight))
        
        parent[node] = node
        rank[node] = 0
    
    # Sort the edges by weight
    edges.sort(key=lambda x: x[2])
    
    for node1, node2, weight in edges:
        # Check if adding the edge will form a cycle
        if find(node1) != find(node2):
            mst.append((node1, node2, weight))
            union(node1, node2)
            
        if len(mst) == len(graph) - 1:
            break
        
    return mst

graph = {
    'A': [('B', 2), ('E', 3)],
    'B': [('A', 2), ('C', 3), ('D', 4)],
    'C': [('B', 3), ('D', 4)],
    'D': [('B', 4), ('C', 4), ('E', 5)],
    'E': [('A', 3), ('D', 5)]
}

mst  = kruskals_algorithm(graph)

# Print the result
print("Minimum Spanning Tree:")
for edge in mst:
    print(f"{edge[0]} - {edge[1]} (weight: {edge[2]})")