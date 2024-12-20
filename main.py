def read_input():
    import sys
    input = sys.stdin.read
    data = input().splitlines()

    n, m, s, L = map(int, data[0].split())
    edges = []
    for line in data[1:]:
        u, v, t, c = map(int, line.split())
        edges.append((u, v, t, c))

    return n, m, s, L, edges

def dijkstra_broadcast(n, edges, source, max_time):
    # Graph representation
    graph = {i: [] for i in range(1, n + 1)}
    for u, v, t, c in edges:
        graph[u].append((v, t, c))
        graph[v].append((u, t, c))  # Undirected graph: edge added both ways

    # Priority queue: (time, cost, current_node, previous_node)
    pq = [(0, 0, source, -1)]

    # Tracking structures
    min_time = {i: float('inf') for i in range(1, n + 1)}
    min_cost = {i: float('inf') for i in range(1, n + 1)}
    visited = set()
    broadcast_tree = []

    min_time[source] = 0
    min_cost[source] = 0

    total_cost = 0

    while pq:
        # Sort by time, then by cost
        pq.sort()
        curr_time, curr_cost, node, parent = pq.pop(0)

        if node in visited:
            continue

        visited.add(node)

        # If this is a valid edge (not the source), add to the broadcast tree
        if parent != -1:
            broadcast_tree.append((parent, node))
            total_cost += curr_cost

        for neighbor, time, cost in graph[node]:
            new_time = curr_time + time
            new_cost = cost

            if new_time <= max_time and neighbor not in visited and new_time < min_time[neighbor]:
                min_time[neighbor] = new_time
                min_cost[neighbor] = new_cost
                pq.append((new_time, new_cost, neighbor, node))

    # Check if all nodes are reachable
    if len(visited) < n:
        return "NO_SOLUTION"

    # Return the total cost
    return total_cost

if __name__ == "__main__":
    # Read inputs
    n, m, s, L, edges = read_input()
    result = dijkstra_broadcast(n, edges, s, L)
    print(result)
