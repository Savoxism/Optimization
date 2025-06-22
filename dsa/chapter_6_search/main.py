import sys

def find_left(arr, k):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < k:
            lo = mid + 1
        else:
            hi = mid
    return lo

def find_right(arr, k):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] <= k:
            lo = mid + 1
        else:
            hi = mid
    return lo

T = []

for line in sys.stdin:
    line = line.strip()
    if not line or line == '#':
        break

    op, s = line.split()
    k = int(s)

    if op == 'insert':
            i = find_left(T, k)
            if i == len(T) or T[i] != k:
                T.insert(i, k)

    elif op == 'remove':
        i = find_left(T, k)
        if i < len(T) and T[i] == k:
            T.pop(i)

    elif op == 'pred-succ':
        i = find_left(T, k)
        if i == len(T) or T[i] != k:
            print(-1, -1)
            continue

        # predecessor
        if i == 0:
            pred = -1
        else:
            pred = T[i-1]

        # successor
        j = find_right(T, k)
        if j == len(T):
            succ = -1
        else:
            succ = T[j]

        print(pred, succ)