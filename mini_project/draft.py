import sys


def read_input():
    input = sys.stdin.read
    data = input().splitlines()

    T, N, M = map(int, data[0].split())
    
    class_subjects = []
    for i in range(1, N + 1):
        class_subjects.append(list(map(int, data[i].split()))[:-1])

    teacher_subjects = []
    for i in range(N + 1, N + T + 1):
        teacher_subjects.append(list(map(int, data[i].split()))[:-1])

    subject_hours = list(map(int, data[N + T + 1].split()))

    return T, N, M, class_subjects, teacher_subjects, subject_hours


T, N, M, class_subjects, teacher_subjects, subject_hours = read_input()

print(T, N, M)
print()
print(class_subjects)
print()
print(teacher_subjects)
print()
print(subject_hours)
print()