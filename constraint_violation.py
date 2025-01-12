import sys

'''
Explaining all the constraints:
1) AllDifferent: This constraint ensures that all variables in the set must have unique values.

2) IsEqual: This constraint ensures that two specific variables must have the same value.

3) LessThanEqual: This constraint ensures that the first variable must be less than or equal to the second variable.

Violations here are calculated by the degree of violation of the constraint, not just a binary value.
'''

"""
7
3 1 2 3 5 4 1
post AllDifferent
violations
post IsEqual 2 5
violations
update 3 1
violations 
post LessThanEqual 5 1
update 1 6
violations
"""

import sys

def read_input():
    input_lines = sys.stdin.read().splitlines()
    
    N = int(input_lines[0])
    
    variables = list(map(int, input_lines[1].split()))
    
    actions = [line for line in input_lines[2:] if line.strip()]

    return N, variables, actions

def solve(N, variables, actions):
    constraints = []  
    
    constraint_funcs = {
        'AllDifferent': lambda vars: sum(count * (count - 1) // 2 for count in {x: vars.count(x) for x in vars}.values()),
        'IsEqual': lambda vars, i, j: abs(vars[i] - vars[j]),
        'LessThanEqual': lambda vars, i, j: max(0, vars[i] - vars[j])
    }
    
    for action in actions:
        
        action = action.split()
        
        if action[0] == 'post':
            constraint_type = action[1]
            if constraint_type == 'AllDifferent':
                constraints.append((constraint_type,))
            else:
                i, j = int(action[2]) - 1, int(action[3]) - 1 
                constraints.append((constraint_type, i, j))

        elif action[0] == 'update':
            index, value = int(action[1]) - 1, int(action[2]) 
            variables[index] = value

        elif action[0] == 'violations':
            total_violations = 0
            for constraint in constraints:
                if constraint[0] == 'AllDifferent':
                    total_violations += constraint_funcs['AllDifferent'](variables)
                else:
                    constraint_type, i, j = constraint
                    total_violations += constraint_funcs[constraint_type](variables, i, j)
            print(total_violations)
    
    
if __name__ == '__main__':
    N, variables, actions = read_input()
    solve(N, variables, actions)
    