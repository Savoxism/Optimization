import sys 

def read_input():
    n = int(sys.stdin.readline().strip())
    
    variables = []
    for i in range(n):
        line = list(map(int, sys.stdin.readline().split()))
        variables.append(Variable(f"X{i + 1}", line[1:]))

    m = int(sys.stdin.readline().strip())

    constraints = []
    for i in range(m):
        xi, xj, d = map(int, sys.stdin.readline().split())
        constraints.append((variables[xi - 1], variables[xj - 1], d))
        constraints.append((variables[xj - 1], variables[xi - 1], -d))

    return variables, constraints

class Variable:
    def __init__(self, name, domain):
        self.name = name
        self.domain = set(domain)
    
    def remove(self, value):
        if value in self.domain:
            self.domain.remove(value)

    def is_empty(self):
        return len(self.domain) == 0

class Constraint:
    def __init__(self, var1, var2, delta):
        self.var1 = var1
        self.var2 = var2
        self.delta = delta

    def is_satisfied(self, val1, val2):
        return val1 <= val2 + self.delta

class ArcConsistency:
    def __init__(self, variables, arcs):
        self.variables = variables
        self.arcs = arcs
        self.agenda = arcs.copy()
        
    def revise(self, arc):
        var1, var2, delta = arc
        revised = False
        to_remove = set()
        
        for val1 in var1.domain:
            satisfies = any(
                val1 <= val2 + delta 
                for val2 in var2.domain
            )
            # If no value in var2's domain satisfies the constraint, remove val1
            if not satisfies:
                to_remove.add(val1)
                revised = True
                
        for val in to_remove:
            var1.remove(val)    
            
        return revised
    
    def run(self):
        while self.agenda:
            arc = self.agenda.pop(0)
            
            var1, var2, _ = arc
            
            if self.revise(arc):
                if var1.is_empty():
                    return False
                
                # This condition ensures that we don't add an arc to the agenda if it's already there and right side of the constraint is the same as the considered variable
                for other_arc in self.arcs:
                    if other_arc[1] == var1 and other_arc not in self.agenda:
                        self.agenda.append(other_arc)
                        
        return True
    
# Read input from stdin
variables, constraints = read_input()

# Create arcs and agenda
arcs = [(c[0], c[1], c[2]) for c in constraints]

print("Initial Arc List:")
for arc in arcs:
    print(f"{arc[0].name} -> {arc[1].name} with D = {arc[2]}")

arc_consistency = ArcConsistency(variables, arcs)

if arc_consistency.run():
    for var in variables:
        sorted_domain = sorted(var.domain)
        print(f"{len(sorted_domain)} {' '.join(map(str, sorted_domain))} ")
else:
    print("FAIL")

