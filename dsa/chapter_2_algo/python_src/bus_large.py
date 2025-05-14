import sys
import random
import time
import math

'''
5 3
0 5 8 11 12 8 3 3 7 5 5 
5 0 3 5 7 5 3 4 2 2 2 
8 3 0 7 8 8 5 7 1 6 5 
11 5 7 0 1 5 9 8 6 5 6 
12 7 8 1 0 6 10 10 7 7 7 
8 5 8 5 6 0 8 5 7 3 4 
3 3 5 9 10 8 0 3 4 5 4 
3 4 7 8 10 5 3 0 6 2 2 
7 2 1 6 7 7 4 6 0 5 4 
5 2 6 5 7 3 5 2 5 0 1 
5 2 5 6 7 4 4 2 4 1 0 
'''

def greedy_initial(n, k, c):
    onboard, delivered = set(), set()
    route, current, load = [0], 0, 0
    todo = set(range(1, n + 1))

    while len(delivered) < n:
        candidates = []
        for p in onboard:
            if p + n not in delivered:
                candidates.append((c[current][p + n], p + n, 'drop', p))
        if load < k:
            for p in todo:
                candidates.append((c[current][p], p, 'pick', p))
        if not candidates:
            break
        candidates.sort()
        _, next_point, action, pid = candidates[0]
        route.append(next_point)
        if action == 'pick':
            onboard.add(pid)
            todo.remove(pid)
            load += 1
        else:
            delivered.add(pid)
            onboard.remove(pid)
            load -= 1
        current = next_point
    route.append(0)
    return route

def is_valid(route, n, k):
    '''
    3 constraints:
        + overloaded passengers
        + passenger can only be dropped off after having been picked up 
        + each passenger is only picked up and dropped off once
    '''
    onboard, load, seen = set(), 0, set()
    for point in route[1:]: # exlcuding the depot 
        # pick up points
        if 1 <= point <= n:
            if load == k: # bus is full
                return False
            load += 1
            onboard.add(point)
            seen.add(point)
        
        elif n < point <= 2 * n:
            passenger = point - n
            if passenger not in seen or passenger not in onboard: # have been picked up & currently on bus
                return False
            load -= 1
            onboard.remove(passenger)
    return True

def perturb(route):
    i = random.randint(1, len(route) - 3)
    j = random.randint(i + 1, len(route) - 2)
    pertubation = route[:i] + route[i:j+1][::-1] + route[j+1:]
    return pertubation
    
def SA(n, k , c, route):
    def cost(r): return sum(c[r[i]][r[i+1]] for i in range(len(r)-1))

    best = list(route)
    best_cost = cost(route)
    current = list(route)
    current_cost = best_cost
    T, alpha = 1000.0, 0.995
    start_time = time.time()
    
    while time.time() - start_time < 3.0:
        candidate = perturb(current)
        
        if not is_valid(candidate, n, k):
            continue
        
        cand_cost = cost(candidate)
        delta = cand_cost - current_cost
        if delta < 0 or random.random() < math.exp(-delta / T):
            current = candidate
            current_cost = cand_cost
            if cand_cost < best_cost:
                best = list(candidate)
                best_cost = cand_cost
            
        T *= alpha
        
    return best


# usage
n, k = map(int, sys.stdin.readline().split())
c = [list(map(int, sys.stdin.readline().split())) for _ in range(2 * n + 1)]
initial = greedy_initial(n, k, c)
sol = SA(n, k, c, initial)

print(n)
print(" ".join(map(str, sol[1:])))
