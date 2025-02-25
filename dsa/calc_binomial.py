def C(n: int, k: int):
    if k == 0 or k == n:
        return 1
    else:
        return C(n - 1, k) + C(n - 1, k - 1)
    
print(C(5, 2))


