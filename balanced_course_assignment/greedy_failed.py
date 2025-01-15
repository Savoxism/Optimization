import sys
"""
4 12
5 1 3 5 10 12
5 9 3 4 8 12
6 1 2 3 4 9 7
7 1 2 3 5 6 10 11
25
1 2
1 3
1 5
2 4
2 5
2 6
3 5
3 7
3 10
4 6
4 9
5 6
5 7
5 8
6 8
6 9
7 8
7 10
7 11
8 9
8 11
8 12
9 12
10 11
11 12
"""

def read_input():
    input = sys.stdin.read().splitlines()
    
    m, n = map(int, input[0].split())
    
    # Preference list
    A = []
    for i in range(1, m + 1):
        line = list(map(int, input[i].split()))
        courses = [x - 1 for x in line[1:]]
        A.append(courses)
    
    # number of conflicts
    k = int(input[m + 1])
    
    # conflict pairs
    B = []
    for i in range(m + 2, m + 2 + k):
        i, j = map(int, input[i].split())
        B.append([i - 1, j - 1]) 
        
    return m, n, A, B

def assign_courses(m, n, A, B):
    conflict_count = [0] * n
    for conflict in B:
        conflict_count[conflict[0]] += 1
        conflict_count[conflict[1]] += 1
    
    sorted_courses = sorted(range(n), key=lambda x: -conflict_count[x])
    
    # Initialize the load for each teacher
    load = [0] * m
    # Initialize the list of assigned courses for each teacher
    assigned = [set() for _ in range(m)]
    
    for course in sorted_courses:
        # eligible teacher with minimal load
        min_load = float('inf')
        best_teacher = -1
        
        for teacher in range(m):
            if course in A[teacher]:
                conflict_found = False
                for assigned_course in assigned[teacher]:
                    if [course, assigned_course] in B or [assigned_course, course] in B:
                        conflict_found = True
                        break
                if not conflict_found and load[teacher] < min_load:
                    min_load = load[teacher]
                    best_teacher = teacher
        
        # if no teacher is eligible            
        if best_teacher == -1:
            return -1
        
        assigned[best_teacher].add(course)
        load[best_teacher] += 1
    
    return max(load)

m, n, A, B = read_input()
result = assign_courses(m, n, A, B)
print(result)