import sys
from io import StringIO

"""
fx = 3 * x1 + 4 * x2

2 * x1 + x2 <= 7
x1 + 2 * x2 <= 8
x1 - x2 <= 2

The contraints have excluded the non-negative constraints for x1 and x2.

2 3
3 4
2 1
1 2
1 -1
7 8 2 
<= >= =
"""

def read_input():
    '''
    n: Number of variables
    m: Number of constraints
    C: Objective function coefficients
    A: Coefficient matrix for constraints
    b: Right-hand side values for constraints
    constraint_types: List of constraint types (<=, >=, =)
    '''
    n, m = map(int, sys.stdin.readline().split())
    
    C = list(map(float, sys.stdin.readline().split()))
    
    A = []
    for _ in range(m):
        row = list(map(float, sys.stdin.readline().split()))
        A.append(row)

    b = list(map(float, sys.stdin.readline().split()))
    
    constraint_types = sys.stdin.readline().strip().split()

    return n, m, C, A, b, constraint_types

def add_slack_and_artificial_variables(A, b, m, constraint_types):
    tableau = []
    num_artificial = 0
    artificial_indices = []
    
    # Number of original variables
    n = len(A[0]) if A else 0
    
    # Count the number of artificial variables needed
    for constraint_type in constraint_types:
        if constraint_type == '>=' or constraint_type == '=':
            num_artificial += 1
    
    for i in range(m):
        # Initialize slack variables for all constraints
        slack = [0] * m  # All slack variables start with coefficient 0
        
        if constraint_types[i] == '<=':
            # Add slack variable for <= constraint
            slack[i] = 1  # Coefficient of 1 for s_i
            # Pad with 0s for artificial variables
            artificial = [0] * num_artificial
            tableau.append(A[i] + slack + artificial + [b[i]])
            
        elif constraint_types[i] == '>=':
            # Add slack variable and artificial variable for >= constraint
            slack[i] = -1  # Coefficient of -1 for s_i
            artificial = [0] * num_artificial
            artificial[num_artificial - 1] = 1  # Coefficient of 1 for the new artificial variable
            tableau.append(A[i] + slack + artificial + [b[i]])
            # Calculate the index of the artificial variable
            artificial_index = n + m + num_artificial - 1
            artificial_indices.append(artificial_index)
            
        elif constraint_types[i] == '=':
            # Add artificial variable for equality constraint
            artificial = [0] * num_artificial
            artificial[num_artificial - 1] = 1  # Coefficient of 1 for the new artificial variable
            tableau.append(A[i] + [0] * m + artificial + [b[i]])
            # Calculate the index of the artificial variable
            artificial_index = n + m + num_artificial - 1
            artificial_indices.append(artificial_index)
            
    return tableau, num_artificial, artificial_indices



# Example input
A = [
    [1, 1],  # Coefficients for constraint 1
    [2, 1],  # Coefficients for constraint 2
    [1, -1]  # Coefficients for constraint 3
]
b = [4, 6, 1]
m = 3
constraint_types = ['<=', '>=', '=']

# Call the corrected function
tableau, num_artificial, artificial_indices = add_slack_and_artificial_variables(A, b, m, constraint_types)

# Print the results
print("Tableau:")
for row in tableau:
    print(row)
print("Number of artificial variables:", num_artificial)
print("Indices of artificial variables:", artificial_indices)











