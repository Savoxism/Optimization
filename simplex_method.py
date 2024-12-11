import sys
"""
n = 2, m = 3

fx = 3 * x1 + 4 * x2

2 * x1 + x2 <= 7
x1 + 2 * x2 <= 8
x1 - x2 <= 2

The contraints have excluded the non-negative constraints for x1 and x2.

2 3
3 2
2 1
1 2
1 -1
7 8 2
"""

def read_inputs():
    n, m = map(int, sys.stdin.readline().split())
    
    C = list(map(float, sys.stdin.readline().split()))

    A = []
    for _ in range(m):
        row = list(map(float, sys.stdin.readline().split()))
        A.append(row)

    b = list(map(float, sys.stdin.readline().split()))

    return n, m, C, A, b

def add_slack_variables(A, b, m):
    tableau = []
    
    for i in range(m):
        # Row format: [original A row, slack variables, RHS]
        slack = [0] * m
        slack[i] = 1 
        tableau.append(A[i] + slack + [b[i]]) 
        
    return tableau

def add_obj_row(tableau, C, n, m):
    obj_row = [-C[i] if i < n else 0 for i in range(n)]
    obj_row += [0] * m
    obj_row += [0] 
    
    # Append the objective row to the tableau
    tableau.append(obj_row)
    return tableau

def simplex_method(tableau, n, m):
    while True:
        # Check for optimality
        if all(c >= 0 for c in tableau[-1][:-1]):
            break
        
        # Obtain the index of the entering variable
        entering = tableau[-1][:-1].index(min(tableau[-1][:-1])) # Column
        
        # Check for unboundedness
        if all(row[entering] <= 0 for row in tableau[:-1]):
            return [], 0, "UNBOUNDED"  
        
        # Choose leaving variable
        ratios = []
        for row in tableau[:-1]: 
            if row[entering] > 0:
                ratio = row[-1] / row[entering]
                ratios.append(ratio) 
            else:
                ratios.append(float('inf')) 
        leaving = ratios.index(min(ratios))
        
        # Perform pivot operation
        pivot = tableau[leaving][entering]
        tableau[leaving] = [x / pivot for x in tableau[leaving]]
        for i, row in enumerate(tableau):
            if i != leaving:
                factor = row[entering]
                for j in range(len(row)): # consider columns
                    tableau[i][j] = row[j] - factor * tableau[leaving][j]
                    
    # Extract solution
    solution = [0] * n
    for i in range(n):
        column = [row[i] for row in tableau[:-1]]  # Exclude objective row
        if column.count(0) == len(column) - 1 and 1 in column:  # Check unit vector
            solution[i] = tableau[column.index(1)][-1]

    # Optimal value is in the RHS of the objective row
    optimal_value = tableau[-1][-1]
    return solution, optimal_value, "OPTIMAL"
        

def solve():
    n, m, C, A, b = read_inputs()
    tableau = add_slack_variables(A, b, m)
    tableau = add_obj_row(tableau, C, n, m)
    
    solution, optimal_value, status = simplex_method(tableau, n, m)
    
    if status == "OPTIMAL":
        print(n)
        print(" ".join(map(str, solution)))  
        # print(optimal_value)
    elif status == "UNBOUNDED":
        print("UNBOUNDED")
        
if __name__ == "__main__":
    solve()