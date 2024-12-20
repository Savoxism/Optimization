'''
Explaining all the constraints:
1) AllDifferent: This constraint ensures that all variables in the set must have unique values.

2) IsEqual: This constraint ensures that two specific variables must have the same value.

3) LessThanEqual: This constraint ensures that the first variable must be less than or equal to the second variable.

Violations here are calculated by the degree of violation of the constraint, not just a binary value.
'''
import sys

def read_input():
    input = sys.stdin.read
    lines = input().strip().split("\n")
    
    n = int(lines[0])
    
    variables = list(map(int, lines[1].split()))
    
    actions = lines[2:]
    
    return n, variables, actions

def calculate_all_different(variables):
    violations = 0
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            if variables[i] == variables[j]:
                violations += 1
    return violations

def calculate_is_equal(x1, x2):
    return abs(x1 - x2)

def calculate_less_than_equal(x1, x2):
    return max(0, x1 - x2)

def process_actions(n, variables, actions):
    all_different_active = False
    is_equal_constraints = [] 
    less_than_equal_constraints = []
    results = []
    
    for action in actions:
        parts = action.split()
        if parts[0] == "post":
            if parts[1] == "AllDifferent":
                all_different_active = True
            elif parts[1] == "IsEqual":
                i, j = int(parts[2]), int(parts[3])
                is_equal_constraints.append((i - 1, j - 1))
            elif parts[1] == "LessThanEqual":
                i, j = int(parts[2]), int(parts[3])
                less_than_equal_constraints.append((i - 1, j - 1))
                
        elif parts[0] == "update":
            i, v, = int(parts[1]), int(parts[2])
            variables[i - 1] = v
            
        elif parts[0] == "violations":
            total_violations = 0
            if all_different_active:
                total_violations += calculate_all_different(variables)
                
            for i, j in is_equal_constraints:
                total_violations += calculate_is_equal(variables[i], variables[j])
            
            for i, j in less_than_equal_constraints:
                total_violations += calculate_less_than_equal(variables[i], variables[j])
            
            results.append(total_violations)
            
    return results


def main():
    n, variables, actions = read_input()
    results = process_actions(n, variables, actions)
    for result in results:
        print(result)

if __name__ == "__main__":
    main()
