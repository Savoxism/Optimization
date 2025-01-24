import sys

def read_input():
    lines = sys.stdin.readlines()
    
    n, k = map(int, lines[0].split())
    
    distance_matrix = []
    for line in lines[1:]:
        distance_matrix.append(list(map(int, line.split())))
    
    return n, k, distance_matrix

def solve(n, k , distance_matrix):
    current_location = 0
    # route = [0]
    route = []
    passengers_on_bus = []
    passengers_picked_up = set()
    passengers_dropped_off = set()
    total_distance = 0
    
    while len(passengers_dropped_off) < n:
        nearest_point = -1
        min_distance = float('inf')
        
        for point in range(2 * n + 1):
            
            if point == current_location:
                continue
            
            if point == 0:
                if len(passengers_dropped_off) == n:
                    pass # prevent premature return to point 0 
                else:
                    continue          
            elif 1 <= point <= n:
                # check whether passenger is already picked up and bus is not full
                if point not in passengers_picked_up and len(passengers_on_bus) < k:
                    pass
                else:
                    continue  
            elif n + 1 <= point <= 2 * n:
                passenger = point - n
                # check whether passenger is on bus and not yet dropped off
                if passenger in passengers_on_bus and passenger not in passengers_dropped_off:
                    pass
                else:
                    continue
            
            # Calculating distance
            distance = distance_matrix[current_location][point]
            if distance < min_distance:
                min_distance = distance
                nearest_point = point
                
        if nearest_point == -1:
            break
        
        total_distance += distance_matrix[current_location][nearest_point]
        
        route.append(nearest_point)
        current_location = nearest_point
        
        if 1 <= nearest_point <= n:
            # pick up passenger
            passengers_on_bus.append(nearest_point)
            passengers_picked_up.add(nearest_point)
        elif n + 1 <= nearest_point <= 2 * n:
            # drop off passenger
            passenger = nearest_point - n
            passengers_on_bus.remove(passenger)
            passengers_dropped_off.add(passenger)
    
    # Return to point 0
    # total_distance += distance_matrix[current_location][0]
    # route.append(0)

    return route, total_distance

n, k, distance_matrix = read_input()
route, total_distance = solve(n, k, distance_matrix)

print(n)
print(' '.join(map(str, route)))
print(total_distance)