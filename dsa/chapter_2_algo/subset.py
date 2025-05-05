import sys

'''
5 5 10
9 4 10 3 7 
'''

n, A, B = map(int, sys.stdin.readline().split())
arr = list(map(int, sys.stdin.readline().split()))
MAX_SUM = sum(arr)

# dp[s] number of subsets whose sum is s
dp = [0] * (MAX_SUM + 1)
dp[0] = 1

for num in arr:
    for s in range(MAX_SUM, num - 1, -1):
        dp[s] += dp[s - num]
        
count = sum(dp[s] for s in range(A, B+1))
print(count)