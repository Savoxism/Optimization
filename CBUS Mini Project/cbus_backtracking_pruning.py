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
    f = 0
    f_star = float('inf')  
    route = [0]  
    best_route = []  
    visited = [False] * (2 * n + 1)  
    load = 0  

    # Precompute the minimum distance between any two points
    C_min = min(
        dist_matrix[i][j]
        for i in range(2 * n + 1)
        for j in range(2 * n + 1)
        if i != j
    )

    # Check if visiting point v at step k is feasible
    def check(vertex, load):
        if visited[vertex]:
            return False
        if vertex > n and not visited[vertex - n]:  # Drop-off point before pick-up point
            return False
        if vertex <= n and load + 1 > k:  # Exceeds bus capacity
            return False
        return True
    
    # Update the best route length and route found so far
    def update_best(f):
        nonlocal f_star, best_route
        if f + dist_matrix[route[-1]][0] < f_star:
            f_star = f + dist_matrix[route[-1]][0]
            best_route = route.copy()  
            
    def backtrack(state, step, f, load):
        nonlocal f_star

        for v in range(1, 2 * n + 1):
            if check(v, load):
                route.append(v)
                f += dist_matrix[state][v]
                visited[v] = True

                if v <= n:  
                    load += 1
                else:  
                    load -= 1

                if step == 2 * n:  
                    update_best(f)
                else:
                    # Pruning: only proceed if lower bound is promising
                    if f + C_min * (2 * n + 1 - step) < f_star:
                        backtrack(v, step + 1, f, load)

                # Backtrack
                if v <= n:
                    load -= 1
                else:
                    load += 1
                f -= dist_matrix[state][v]
                visited[v] = False
                route.pop()
        
    backtrack(0, 1, f, load)
    return f_star, best_route

n, k, dist_matrix = read_input()
result, route = CBUS(n, k, dist_matrix)

print(n)
print(result)
print(" ".join(map(str, route[1:])))  