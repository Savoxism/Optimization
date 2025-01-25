def multistage(graph, stages, start, end):
    num_nodes = max(graph.keys())
    cost = [[float('inf')] * (num_nodes + 1) for _ in range(stages + 1)]
    cost[stages][end] = 0
    
    # Step 1: Backward traversal to compute costs
    for stage in range(stages, 0, -1):  # Traverse backward from last stage to first
        for node in graph:
            for neighbor, weight in graph[node]:
                if stage < stages:
                    cost[stage][node] = min(cost[stage][node], weight + cost[stage + 1][neighbor])

    # Step 2: Path reconstruction
    path = [start]
    current_node = start
    current_stage = 1 

    while current_node != end:
        for neighbor, weight in graph[current_node]:
            # Use the dynamically computed stage
            if cost[current_stage][current_node] == weight + cost[current_stage + 1][neighbor]:
                path.append(neighbor)
                current_node = neighbor
                current_stage += 1 
                break

    return path


stages = 5
start = 1
end = 12
graph = {
    1: [(2, 9), (3, 7), (4, 3), (5, 2)],
    2: [(6, 4), (7, 2), (8, 1)],
    3: [(6, 2), (7, 7)],
    4: [(8, 11)],
    5: [(7, 11),(8, 8)],
    6: [(9, 6), (10, 5)],
    7: [(9, 4), (10, 3)],
    8: [(10, 5), (11, 6)],
    9: [(12, 4)],
    10: [(12, 2)],
    11: [(12, 5)],
    12: [] 
}

print(multistage(graph, stages, start, end))  
