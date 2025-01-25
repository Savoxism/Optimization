import sys

'''
4 3
1 2 -1 1
1 1 -1 -1
1 0 1 1
1 -1 -1 0
4 7 2
= = =
'''

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
            artificial[len(artificial_indices)] = 1  # Coefficient of 1 
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

def simplex_method_phase1(tableau, artificial_indices):
    while True:
        if all(c >= 0 for c in tableau[-1][:-1]):
            break
        
        entering = tableau[-1][:-1].index(min(tableau[-1][:-1]))  # Column index
        
        # Check for unboundedness
        if all(row[entering] <= 0 for row in tableau[:-1]):
            return tableau, "INFEASIBLE"
        
        # Choose leaving variable (minimum ratio test)
        ratios = []
        for row in tableau[:-1]:
            if row[entering] > 0:
                ratio = row[-1] / row[entering]
                ratios.append(ratio)
            else:
                ratios.append(float('inf'))
        leaving = ratios.index(min(ratios))  # Row index
        
        # Perform pivot operation
        pivot = tableau[leaving][entering]
        tableau[leaving] = [x / pivot for x in tableau[leaving]]
        for i, row in enumerate(tableau):
            if i != leaving:
                factor = row[entering]
                tableau[i] = [row[j] - factor * tableau[leaving][j] for j in range(len(row))]
    
    # Check if Phase 1 was successful (optimal value should be 0)
    optimal_value = tableau[-1][-1]
    if abs(optimal_value) > 1e-6: 
        return tableau, "INFEASIBLE"
    
    # Remove artificial variables and Phase 1 objective row
    new_tableau = []
    for row in tableau[:-1]: 
        new_row = [row[j] for j in range(len(row)) if j not in artificial_indices]
        new_tableau.append(new_row)
    
    return new_tableau, "PHASE1_COMPLETE"

### PHASE 2 ###
def add_phase2_objective_row(tableau, c):
    objective_row = [0] * len(tableau[0]) 
    objective_row[-2] = 1  # Coefficient of 1 for z-column
    
    for i in range(len(c)):
        objective_row[i] = -c[i]
        
    tableau.append(objective_row)
    return tableau

def simplex_method_phase2(tableau, n):
    while True:
        if all(c >= 0 for c in tableau[-1][:-1]):
            break
    
        entering = tableau[-1][:-1].index(min(tableau[-1][:-1]))  # Column index
        
        if all(row[entering] <= 0 for row in tableau[:-1]):
            return [], 0, "UNBOUNDED"

        ratios = []
        for row in tableau[:-1]:
            if row[entering] > 0:
                ratio = row[-1] / row[entering]
                ratios.append(ratio)
            else:
                ratios.append(float('inf'))
        leaving = ratios.index(min(ratios))  # Row index
        
        # Perform pivot operation
        pivot = tableau[leaving][entering]
        tableau[leaving] = [x / pivot for x in tableau[leaving]]  # Make pivot element 1
        for i, row in enumerate(tableau):
            if i != leaving:
                factor = row[entering]
                tableau[i] = [row[j] - factor * tableau[leaving][j] for j in range(len(row))]
                
    solution = [0] * n
    for i in range(n):
        column = [row[i] for row in tableau[:-1]]  # Exclude objective row
        if column.count(0) == len(column) - 1 and 1 in column:  # Check unit vector
            solution[i] = tableau[column.index(1)][-1]
    
    # Optimal value is in the RHS of the objective row
    optimal_value = tableau[-1][-1]
    
    return solution, optimal_value, "OPTIMAL"

def solve(A, b, m, constraint_types, c):
    tableau, _, artificial_indices = add_slack_and_artificial_variables(A, b, m, constraint_types)
    
    tableau = add_phase1_objective_row(tableau, artificial_indices)
    
    tableau = update_tableau(tableau)

    tableau, status = simplex_method_phase1(tableau, artificial_indices)
    
    if status == "INFEASIBLE":
        return [], 0, "INFEASIBLE"
    
    for row in tableau:
        row.insert(-1, 0)  # Insert 0 for z-column just before the RHS column
    
    tableau = add_phase2_objective_row(tableau, c)
        
    n = len(c) 
    solution, optimal_value, status = simplex_method_phase2(tableau, n)
     
    return solution, optimal_value, status


# Example input
# n, m = 4, 3
# C = [1, 2, -1, 1]
# A = [
#     [1, 1, -1, -1],  # Coefficients for constraint 1
#     [1, 0, 1, 1],  # Coefficients for constraint 2
#     [1, -1, -1, 0]  # Coefficients for constraint 3
# ]
# b = [4, 7, 2]
# constraint_types = ['=', '=', '=']

if __name__ == "__main__":
    n, m, C, A, b, constraint_types = read_input()
    solution, optimal_value, status = solve(A, b, m, constraint_types, C)
    print(f"Solutions are: {solution}")
    print("The optimal value is:", optimal_value)
    print(status)
