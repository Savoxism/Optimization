import sys
from collections import deque

def read_input():
    input = sys.stdin.read().splitlines()
    
    n = int(input[0])
    
    domain = {}
    for i in range(n):
        t = [int(x) for x in input[i + 1].split()]
        domain[f"x{i+1}"] = t[1:]
        
    m = int(input[n + 1])
    constraints = []
    for i in range(m):
        temp = [int(x) for x in input[n + i + 2].split()]   
        constraints.append((f"x{temp[0]}", f"x{temp[1]}", temp[2]))
    
    return n, domain, m, constraints

def AC3(domain, constraints):
    queue = deque(constraints)
    
    while queue:
        ele = queue.popleft() # leftmost element 
        if reviseAC3(ele, domain):
            # Check if the domain of x_i or x_j has become empty
            if not domain[ele[0]] or not domain[ele[1]]:
                return False
            else:
                for constraint in constraints:
                    # This condition checks if the current constraint (ele) is related to another constraint in the list.
                    if (ele[0] in constraint or ele[1] in constraint) and constraint != ele:
                        queue.append(constraint)
    
    return True

def reviseAC3(ele, domain):
    changed = False
    
    # Check for Xi <= Xj + D
    for value0 in domain[ele[0]].copy():
        found = False
        for value1 in domain[ele[1]]:
            if value0 <= value1 + ele[2]:
                found = True
                break
        
        if found == False:
            domain[ele[0]].remove(value0)
            changed = True
            
    # Check for Xj >= Xi - D
    for value1 in domain[ele[1]].copy():
        found = False
        for value0 in domain[ele[0]]:
            if value1 >= value0 - ele[2]:
                found = True
                break
        
        if found == False:
            domain[ele[1]].remove(value1)
            changed = True
            
    return changed

def solve(n, domain, m, constraints):
    if AC3(domain, constraints):
       for var in sorted(domain.keys()):
           values = sorted(domain[var])
           print(len(values), end=" ")
           print(*values)
    else:
        print("FAIL")
        
if __name__ == "__main__":
    n, domain, m, constraints = read_input()
    solve(n, domain, m, constraints)