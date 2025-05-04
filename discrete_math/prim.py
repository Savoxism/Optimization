
def prims_algorithm(graph, start_node):
    mst = []
    visited = set()
    edges = []
    
    # Start with the start node
    visited.add(start_node)
    edges.extend([(start_node, neighbor, weight) for neighbor, weight in graph[start_node]])
    
    while edges:
        # Find the edge with the smallest weight
        edges.sort(key=lambda x: x[2])
        smallest_edge = edges.pop(0)
        
        u, v, weight = smallest_edge
        
        # If it will connect with the existing node, skip
        if v in visited:
            continue
        
        mst.append(smallest_edge)
        visited.add(v)
        
        for neighbor, weight in graph[v]:
            if neighbor not in visited:
                edges.append((v, neighbor, weight))
                
    return mst
        
    
graph = {
    'A': [('B', 2), ('E', 3)],
    'B': [('A', 2), ('C', 3), ('D', 4)],
    'C': [('B', 3), ('D', 4)],
    'D': [('B', 4), ('C', 4), ('E', 5)],
    'E': [('A', 3), ('D', 5)]
}

start_node = 'A'
mst = prims_algorithm(graph, start_node)

# Print the result
print("Minimum Spanning Tree:")
for edge in mst:
    print(f"{edge[0]} - {edge[1]} (weight: {edge[2]})")