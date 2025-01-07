def a_star_search(graph, heuristics, start, goal):
    open_set = [(start, 0)]
    
    g_score = {node: float("inf") for node in graph}
    g_score[start] = 0
    came_from = {}
    
    while open_set:
        current = min(open_set, key=lambda x: g_score[x[0]] + heuristics[x[0]])[0] # f(n) = g(n) + h(n)
        
        # if current = goal -> path reconstruction
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
                
            path.append(start)
            path.reverse()
            
            return path, g_score[goal]
        
        # Remove the current node from the open set
        open_set = [node for node in open_set if node[0] != current]
        
        for neighbor, cost in graph[current]:
            tentative_g_score = g_score[current] + cost # g(n)

            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score

                open_set.append((neighbor, g_score[neighbor]))
                
    return None, float("inf")

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

path, cost = a_star_search(graph, heuristics, start, goal)
print("Path:", path)
print("Cost:", cost)