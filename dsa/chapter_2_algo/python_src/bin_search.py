
def binsearch(low, high, S, key):
    if low <= high:
        mid = (low + high) // 2

        if S[mid] == key:
            return mid
        
        elif key < S[mid]:
            return binsearch(low, mid - 1, S, key)
        else:
            return binsearch(mid + 1, high, S, key)
    else:
        return -1

S = list(range(0, 10001))
key = 9975
result = binsearch(0, len(S) - 1, S, key)
print("Index of {}: {}".format(key, result))