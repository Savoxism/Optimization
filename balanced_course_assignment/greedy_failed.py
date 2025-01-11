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
    
    # Number of teachers and courses
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

def solve(m, n, A, B):
    load = [0] * m
    
    conflict_graph = {i: set() for i in range(n)}
    for u, v in B:
        conflict_graph[u].add(v)
        conflict_graph[v].add(u)
        
    # Sort courses by the number of conflicts (descending order)
    sorted_courses = sorted(range(n), key=lambda x: len(conflict_graph[x]), reverse=True)
    
    for course in sorted_courses:
        eligible_teachers = [teacher for teacher in range(m) if course in A[teacher]]
        
        min_load = 9999999
        selected_teacher = -1
        
        for teacher in eligible_teachers:
            # Choose the teacher with the minimum load
            if load[teacher] < min_load:
                has_conflict = False
                for assigned_course in A[teacher]:
                    if assigned_course in conflict_graph[course]:
                        has_conflict = True
                        break
                    
                if not has_conflict:
                    min_load = load[teacher]
                    selected_teacher = teacher
                    
        if selected_teacher == -1:
            return -1
        
        load[selected_teacher] += 1
    
    return max(load)

if __name__ == "__main__":
    m, n, A, B = read_input()
    result = solve(m, n, A, B)
    print(result)