import sys

'''
4
0 1 1 9
1 0 9 3
1 9 0 2
9 3 2 0
'''

def read_input():
    input = sys.stdin.read().splitlines()
    n = int(input[0])
    
    cost_matrix = []
    
    for row in input[1:]:
        row = [int(x) for x in row.split()]
        cost_matrix.append(row)
        
    cost_matrix.remove(cost_matrix[-1])
    
    return n, cost_matrix

def greedy2(n, cost_matrix):
    visited = [False] * n
    tour = []
    current_city = 0
    total_cost = 0
    
    for _ in range(n):
        visited[current_city] = True
        tour.append(current_city)
        
        min_cost = 10e9
        next_city = -1
        
        for neighbor in range(n):
            if not visited[neighbor] and cost_matrix[current_city][neighbor] < min_cost:
                min_cost = cost_matrix[current_city][neighbor]
                next_city = neighbor
        
        # Finalize choosing the next city
        if next_city != -1:
            total_cost += min_cost
            current_city = next_city
    
    total_cost += cost_matrix[current_city][0]
    # tour.append(0)
    
    return tour, total_cost

if __name__ == "__main__":
    n, cost_matrix = read_input()
    tour, total_cost = greedy2(n, cost_matrix)
    
    # print(n)
    # print(" ".join(str(x + 1) for x in tour))
    print(total_cost)