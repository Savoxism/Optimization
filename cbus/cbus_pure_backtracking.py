import sys

def read_input():
    lines = sys.stdin.read().strip().split("\n")
    
    n, k = map(int, lines[0].split())
    dist_matrix = []
    for line in lines[1:]:
        row = list(map(int, line.split()))
        dist_matrix.append(row)
        
    return n, k, dist_matrix

def solve(n, k, dist_matrix):
    # Global variables
    best_route = None
    best_distance = float('inf')

    def backtrack(current_location, passengers_on_bus, passengers_picked_up, passengers_dropped_off, route, current_distance):
        nonlocal best_route, best_distance

        # Base case
        if len(passengers_dropped_off) == n and current_location == 0:
            if current_distance < best_distance:
                best_distance = current_distance
                best_route = route.copy()
            return

        # Explore all feasible points
        for point in range(2 * n + 1):
            if point == current_location:
                continue  

            if point == 0:
                if len(passengers_dropped_off) < n:
                    continue
            elif 1 <= point <= n:
                if point in passengers_picked_up or len(passengers_on_bus) >= k:
                    continue
            elif n + 1 <= point <= 2 * n:
                passenger = point - n
                if passenger not in passengers_on_bus or passenger in passengers_dropped_off:
                    continue

            # Update state
            route.append(point)
            if 1 <= point <= n:
                passengers_on_bus.append(point)
                passengers_picked_up.add(point)
            elif n + 1 <= point <= 2 * n:
                passenger = point - n
                passengers_on_bus.remove(passenger)
                passengers_dropped_off.add(passenger)

            # Recurse
            backtrack(point, passengers_on_bus, passengers_picked_up, passengers_dropped_off, route, current_distance + dist_matrix[current_location][point])

            # Backtrack (undo changes)
            route.pop()
            if 1 <= point <= n:
                passengers_on_bus.pop()
                passengers_picked_up.remove(point)
            elif n + 1 <= point <= 2 * n:
                passenger = point - n
                passengers_on_bus.append(passenger)
                passengers_dropped_off.remove(passenger)
                
    backtrack(0, [], set(), set(), [0], 0)

    return best_route, best_distance

n, k, dist_matrix = read_input()    
route, total_distance = solve(n, k, dist_matrix)

print(n)
print(" ".join(map(str, route)))
print(total_distance)