def ida_star(graph, heuristics, start, goal):
    def dfs(node, g, threshold):
        nonlocal min_threshold 
        f = g + heuristics[node]
        
        # Pruning
        if f > threshold:
            return None, f # save the f(n) value 
    
        if node == goal:
            return [node], g

        min_threshold = float("inf")

        for neighbor, cost in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                path, cost_found = dfs(neighbor, g + cost, threshold)
                if path:
                    return [node] + path, cost_found
                if cost_found < min_threshold:
                    min_threshold = cost_found
                visited.remove(neighbor)
        
        return None, min_threshold

    threshold = heuristics[start]
    visited = set()
    visited.add(start)
    min_threshold = float("inf")  
    
    while True:
        result, new_threshold = dfs(start, 0, threshold)
        
        if result:
            return result, new_threshold
        
        # no path is found -> failure
        if new_threshold == float("inf"):
            return None, float("inf")
        
        # Suppose every f(n) > threshold and there is no more branches to go, update the threshold to the smallest f(n) value that exceeded the previous threshold 
        threshold = new_threshold
        
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

start = "HB"
goal = "NB"

path, cost = ida_star(graph, heuristics, start, goal)
print("Path:", path)
print("Cost:", cost)