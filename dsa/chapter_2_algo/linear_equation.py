import sys

'''
3 5
'''

input = sys.stdin.readline

n, M = map(int, input().split())
arr = [0] * n

def backtrack(i, total_left):
    # print(f"backtrack(i={i}, total_left={total_left}), current arr = {arr}")
    if i == n - 1: # just print the last element as the total left 
        arr[i] = total_left
        print(*arr)
        return
    
    for x in range(1, total_left - (n - i - 1) + 1):
        arr[i] = x
        # print(f"--> Trying x = {x} at position {i}")
        backtrack(i + 1, total_left - x)
        # print(f"<-- Backtracking from position {i+1} to {i}, reset x = {x}")

backtrack(0, M)

        
    