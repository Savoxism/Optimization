import sys

def read_input():
    lines = sys.stdin.read().strip().split("\n")
    
    n, k = map(int, lines[0].split())
    dist_matrix = []
    for line in lines[1:]:
        row = list(map(int, line.split()))
        dist_matrix.append(row)
        
    return n, k, dist_matrix

def CBUS(n, k, dist_matrix):
    # Global variables
    f = 0
    f_star = float('inf')
    route = [None] * (2 * n + 1)
    visited = [None] * (2 * n + 1)
    load = 0 # Current passengers on the bus
    C_min = min(
        dist_matrix[i][j]
        for i in range(2 * n + 1)
        for j in range(2 * n + 1)
        if i != j
    )  # Minimum distance between any two points 
    
    # Check if visiting point v at step k is feasible
    def check(vertex, load):
        if visited[vertex]:
            return False
        if vertex > n and not visited[vertex - n]:  # Drop-off point before pick-up point
            return False
        if vertex <= n and load + 1 > k:  # Exceeds bus capacity
            return False
        return True
    
    # Update the best route length found so far.
    def update_best(f):
        nonlocal f_star
        if f + dist_matrix[route[2 * n]][0] < f_star:
            f_star = f + dist_matrix[route[2 * n]][0]
            
    def backtrack(state, step, f, load):
        nonlocal f_star

        for vertex in range(1, 2 * n + 1):
            if check(vertex, load):
                route[step] = vertex
                f += dist_matrix[state][vertex]
                visited[vertex] = True

                if vertex <= n:
                    load += 1
                else:
                    load -= 1

                if step == 2 * n:  # All points visited
                    update_best(f)
                else:
                    # Pruning: only proceed if lower bound is promising
                    if f + C_min * (2 * n + 1 - step) < f_star:
                        backtrack(vertex, step + 1, f, load)

                # Backtrack
                if vertex <= n:
                    load -= 1
                else:
                    load += 1
                f -= dist_matrix[state][vertex]
                visited[vertex] = False
        
    backtrack(0, 1, f, load)
    return f_star

if __name__ == "__main__":
    n, k, dist_matrix = read_input()
    result = CBUS(n, k, dist_matrix)
    print("Shortest Route Length:", result)

        
        

