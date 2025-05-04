import math

def dijkstra(graph, start_node):
    distances = {node: math.inf for node in graph}
    distances[start_node] = 0
    
    visited = set()
    priority_queue = [(0, start_node)]
    
    while priority_queue:
        # Get the node with the smallest distance
        priority_queue.sort()
        current_distance, current_node = priority_queue.pop(0)
        
        # Skip if already visited
        if current_node in visited:
            continue
        visited.add(current_node)
        
        for neighbor, weight in graph[current_node]:
            if neighbor not in visited:
                new_distance = current_distance + weight
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    priority_queue.append((new_distance, neighbor))
                    
    return distances      


graph = {
    'A': [('B', 1), ('C', 4)],
    'B': [('A', 1), ('C', 2), ('D', 6)],
    'C': [('A', 4), ('B', 2), ('D', 3)],
    'D': [('B', 6), ('C', 3)]
}

start_node = 'A'
shortest_distances = dijkstra(graph, start_node)

print("Shortest distances from node A:")
for node, distance in shortest_distances.items():
    print(f"{node}: {distance}")
