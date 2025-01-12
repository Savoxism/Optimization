import sys

def read_input():
    input = sys.stdin.read().splitlines()
    
    # m: teachers, n: courses
    m, n = map(int, input[0].split())
    
    # Preference list
    A = []
    for i in range(1, m + 1):
        line = list(map(int, input[i].split()))
        courses = line[1:]  # Use 1-based indexing for courses
        A.append(courses)
    
    # number of conflicts
    k = int(input[m + 1])
    
    # Conflict pairs
    B = []
    for i in range(m + 2, m + 2 + k):
        u, v = map(int, input[i].split())
        B.append([u, v])  # Use 1-based indexing for conflict pairs
        
    return m, n, A, B

m, n, A, B = read_input()

print("The number of teachers is", m)   
print("The number of courses is", n)
print("The preference list is", A)
print("The conflict pairs are", B)
