import sys

def read_inputs():
    """
    Read inputs using sys.stdin.readline() line by line.
    Line 1: n (decision variables), m (constraints)
    Line 2: Coefficients of the objective function (C)
    Next m lines: Rows of the constraint matrix (A)
    Last line: RHS values of the constraints (b)
    """
    # First line: Read n (decision variables) and m (constraints)
    n, m = map(int, sys.stdin.readline().split())

    # Second line: Read the coefficients of the objective function (C)
    C = list(map(float, sys.stdin.readline().split()))

    # Next m lines: Read the rows of the constraint matrix (A)
    A = []
    for _ in range(m):
        row = list(map(float, sys.stdin.readline().split()))
        A.append(row)

    # Last line: Read the RHS values of the constraints (b)
    b = list(map(float, sys.stdin.readline().split()))

    return n, m, C, A, b

n, m, C, A, b = read_inputs()

print(n)
print("_________")
print(m)
print("_________")
print(C)
print("_________")
print(A)
print("_________")
print(b)