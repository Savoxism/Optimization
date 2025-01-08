import sys

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

### PHASE 1 ###

def add_slack_and_artificial_variables(A, b, m, constraint_types):
    tableau = []
    num_artificial = 0
    artificial_indices = []
    
    n = len(A[0]) if A else 0
    
    for constraint_type in constraint_types:
        if constraint_type == '>=' or constraint_type == '=':
            num_artificial += 1
    
    for i in range(m):
        slack = [0] * m  # Coefficient 0 initially 
        
        if constraint_types[i] == '<=':
            slack[i] = 1  # Coefficient of 1 
            artificial = [0] * num_artificial
            tableau.append(A[i] + slack + artificial + [0, b[i]])
            
        elif constraint_types[i] == '>=':
            slack[i] = -1  # Coefficient of -1 
            artificial = [0] * num_artificial
            artificial[len(artificial_indices)] = 1  # Coefficient of 1 
            tableau.append(A[i] + slack + artificial + [0, b[i]])

            artificial_index = n + m + len(artificial_indices)
            artificial_indices.append(artificial_index)
            
        elif constraint_types[i] == '=':
            artificial = [0] * num_artificial
            artificial[len(artificial_indices)] = 1  # Coefficient of 1 for the new artificial variable
            tableau.append(A[i] + [0] * m + artificial + [0, b[i]])
            artificial_index = n + m + len(artificial_indices)
            artificial_indices.append(artificial_index)
            
    return tableau, num_artificial, artificial_indices

def add_phase1_objective_row(tableau, artificial_indices):
    objective_row = [0] * len(tableau[0])
    
    g_column_index = len(tableau[0]) - 2
    objective_row[g_column_index] = 1  # Coefficient of 1 
    
    for idx in artificial_indices:
        objective_row[idx] = 1
        
    tableau.append(objective_row)
    
    return tableau

def update_tableau(tableau):
    objective_row = tableau[-1]
    
    for row_index in range(len(tableau) - 1):
        row_to_subtract = tableau[row_index]
        for i in range(len(objective_row)):
            objective_row[i] -= row_to_subtract[i]
            
    tableau[-1] = objective_row
    
    return tableau


# Example input
A = [
    [1, 1, -1, -1],  # Coefficients for constraint 1
    [1, 0, 1, 1],  # Coefficients for constraint 2
    [1, -1, -1, 0]  # Coefficients for constraint 3
]
b = [4, 7, 2]
m = 3
constraint_types = ['=', '=', '=']

# Step 1: Add slack and artificial variables
tableau, num_artificial, artificial_indices = add_slack_and_artificial_variables(A, b, m, constraint_types)

# Print the initial tableau
print("Initial Tableau:")
for row in tableau:
    print(row)
print("Number of artificial variables:", num_artificial)
print("Indices of artificial variables:", artificial_indices)

# Step 2: Add the Phase 1 objective row
updated_tableau = add_phase1_objective_row(tableau, artificial_indices)

# Print the updated tableau
print("\nUpdated Tableau:")
for row in updated_tableau:
    print(row)

# Step 3: Update the tableau
updated_tableau = update_tableau(updated_tableau)

# Print the updated tableau
print("\nUpdated Tableau 2 :")
for row in updated_tableau:
    print(row)
    
