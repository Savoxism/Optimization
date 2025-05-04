
def floyd_warshall(distance_matrix):
    n = len(distance_matrix)
    
    dist = [[distance_matrix[i][j] for j in range(n)] for i in range(n)]
    
    for k in range(n):
        for i in range(n):
            for j in range(n):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
                
    return dist


distance_matrix = [
    [0, 3, float('inf'), 7],
    [8, 0, 2, float('inf')],
    [5, float('inf'), 0, 1],
    [2, float('inf'), float('inf'), 0]
]

# Run the Floyd-Warshall algorithm
shortest_paths = floyd_warshall(distance_matrix=distance_matrix)

# Print the resulting shortest path matrix
for row in shortest_paths:
    print(row)