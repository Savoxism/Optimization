import math

# Graph representation (Adjacency List)
graph = {
    "LC": [("ST", 20), ("V", 100)],
    "ST": [("LC", 20), ("HN", 5)],
    "HN": [("ST", 5), ("ND", 10), ("HB", 7), ("TB", 15)],
    "HB": [("HN", 7), ("LS", 17), ("HP", 30), ("QN", 90)],
    "LS": [("HB", 17)],
    "HP": [("HB", 30), ("QN", 15), ("TB", 10), ("TH", 80)],
    "QN": [("HP", 15), ("HB", 90), ("V", 90)],
    "ND": [("HN", 10), ("TB", 10), ("NB", 15)],
    "TB": [("ND", 10), ("NB", 15), ("HN", 15), ("HP", 10)],
    "NB": [("ND", 15), ("TB", 15), ("TH", 25)],
    "TH": [("NB", 25), ("V", 15), ("HP", 80)],
    "V": [("TH", 15), ("LC", 100), ("QN", 90)],
}

# Heuristic values for each node
heuristics = {
    "HN": 50,
    "ST": 60,
    "LC": 75,
    "HB": 65,
    "LS": 70,
    "HP": 80,
    "QN": 80,
    "ND": 45,
    "TB": 55,
    "NB": 20,
    "TH": 15,
    "V": 0,
}

def rbfs(node, goal, path, cost, f_limit):
    print(f"Current Node: {node}, Path: {path}, Cost: {cost}, F-limit: {f_limit}")
    
    if node == goal:
        return path, cost 
    
    successors = []
    for neighbor, edge_cost in graph[node]:
        g = cost + edge_cost # Actual cost from start to neighbor 
        h = heuristics[neighbor] # Heuristic cost from neighbor to goal
        f = g + h
        
        successors.append((f, g, neighbor))
        
    if not successors:
        return None, math.inf  # No successors, return failure
    
    successors.sort()
    
    while True:
        best_f, best_g, best_node = successors[0]
        
        if best_f > f_limit:
            return None, best_f
        
        # Get the second best f-value (for backtracking)
        alt_f = successors[1][0] if len(successors) > 1 else math.inf
        
        # Recursive call for the best successor
        result, best_f = rbfs(best_node, goal, path + [best_node], best_g, min(f_limit, alt_f))
        
        if result is not None:
            return result, best_f 
        
        # Update the best f-value and continue
        successors[0] = (best_f, best_g, best_node)
        
        successors.sort()
        
        
# Start and goal nodes
start = "HN"
goal = "V"

# Initial call to RBFS
path, cost = rbfs(start, goal, [start], 0, math.inf)

# Output the result
if path:
    print("Path found:", path)
    print("Total cost:", cost)
else:
    print("No path found.")