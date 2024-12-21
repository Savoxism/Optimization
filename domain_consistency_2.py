import sys

class Variable:
    def __init__(self, domain, name):
        self.domain = set(domain)
        self.name = name

    def remove(self, value):
        self.domain.discard(value)

    def is_empty(self):
        return len(self.domain) == 0

class Constraint:
    def __init__(self, var1, var2, delta, name):
        self.var1 = var1
        self.var2 = var2
        self.delta = delta
        self.name = f"{name} ({var1.name} <= {var2.name} + {delta})"

    def involves(self, variable):
        return variable == self.var1 or variable == self.var2

    def is_satisfied(self, val1, val2):
        return val1 <= val2 + self.delta

    def get_other_variable(self, variable):
        if variable == self.var1:
            return self.var2
        elif variable == self.var2:
            return self.var1
        return None


class ArcConsistency:
    def __init__(self):
        self.constraints = []
        self.agenda = []

    def add_constraint(self, constraint):
        self.constraints.append(constraint)

    def contains_in_agenda(self, variable, constraint):
        return any(var == variable and cons == constraint for var, cons in self.agenda)

    def ac3(self):
        self.agenda = [(variable, constraint)
                       for constraint in self.constraints
                       for variable in (constraint.var1, constraint.var2)
                       ]
        print("Initial Agenda:")
        for var, cons in self.agenda:
            print(f"  {cons.name} involving {var.name}")

        while self.agenda:
            print("\nCurrent Agenda:")
            for var, cons in self.agenda:
                print(f"  {cons.name} involving {var.name}")
            
            variable, constraint = self.agenda.pop(0)
            print(f"\nProcessing: {constraint.name} for {variable.name}")
            
            if self.revise(variable, constraint):
                print(f"Domain revised for {variable.name}: {variable.domain}")
                if variable.is_empty():
                    print(f"FAIL: {variable.name} domain is empty.")
                    return False
                for other_constraint in self.constraints:
                    if other_constraint != constraint and other_constraint.involves(variable):
                        other_var = other_constraint.get_other_variable(variable)
                        if not self.contains_in_agenda(other_var, other_constraint):
                            self.agenda.append((other_var, other_constraint))
                            print(f"  Added {other_constraint.name} involving {other_var.name} to agenda.")
        return True

    def revise(self, variable, constraint):
        other_variable = constraint.get_other_variable(variable)
        to_remove = []
        print(f"  Revising {variable.name} with {other_variable.name}. Current domain: {variable.domain}")
        
        for val in variable.domain:
            if variable == constraint.var1:
                satisfies = any(constraint.is_satisfied(val, other_val)
                                for other_val in other_variable.domain)
            else:
                satisfies = any(constraint.is_satisfied(other_val, val)
                                for other_val in other_variable.domain)

            if not satisfies:
                to_remove.append(val)

        for value in to_remove:
            print(f"    Removing {value} from {variable.name}")
            variable.remove(value)

        return bool(to_remove)


# Input processing
[n] = [int(x) for x in sys.stdin.readline().split()]
variables = []
arc_consistency = ArcConsistency()

# Read variables and their domains
for i in range(n):
    line = [int(x) for x in sys.stdin.readline().split()]
    domain = set(line[1:])
    variable = Variable(domain, f"X{i + 1}")
    variables.append(variable)

# Read constraints
[m] = [int(x) for x in sys.stdin.readline().split()]
for k in range(m):
    i, j, d = [int(x) for x in sys.stdin.readline().split()]
    constraint = Constraint(variables[i - 1], variables[j - 1], d, f"Constraint{k + 1}")
    arc_consistency.add_constraint(constraint)

# Run AC-3 algorithm
if not arc_consistency.ac3():
    print("FAIL")
else:
    print("\nFinal Domains:")
    for variable in variables:
        sorted_domain = sorted(variable.domain)
        print(f"{variable.name}: {sorted_domain}")
        print(len(sorted_domain), *sorted_domain)
