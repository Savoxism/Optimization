import sys

def read_input():
    n = int(sys.stdin.readline().strip())
    cost_matrix = []
    
    for _ in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        row.append(row[0])
        cost_matrix.append(row)
        
    cost_matrix.append(cost_matrix[0])
    
    return n, cost_matrix 

def nearest_neighbor_tsp(n, cost_matrix):
    visited = [False] * n
    tour = []
    current_city = 0
    total_cost = 0
    
    for _ in range(n):
        visited[current_city] = True
        tour.append(current_city)
        
        min_cost = 9999999
        next_city = -1
        
        for neighbor in range(n):
            if not visited[neighbor] and cost_matrix[current_city][neighbor] < min_cost:
                min_cost = cost_matrix[current_city][neighbor]
                next_city = neighbor 
                
        if next_city != -1:
            total_cost += min_cost
            current_city = next_city
            
    # add the cost to return to the starting city
    total_cost += cost_matrix[current_city][0]
    tour.append(0)
    
    return tour, total_cost

n, cost_matrix = read_input()

tour, total_cost = nearest_neighbor_tsp(n, cost_matrix)

new_tour = ' '.join(str(city) for city in tour)

print(new_tour)
print(total_cost)
