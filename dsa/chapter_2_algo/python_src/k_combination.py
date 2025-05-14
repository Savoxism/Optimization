import sys

# dp[j][s]: number of ways to choose j elements such that sum = s
# in the test case, j will run from 0 to 5 

'''
5 3 10
1 2 3 4 5
'''

input = sys.stdin.readline

n, k, m = map(int, input().split())
a = list(map(int, input().split()))

dp = [[0] * (m + 1) for _ in range(k + 1)]
dp[0][0] = 1

for val in a:
    for j in range(k, 0, -1): # choose j elements from k to 1
        for s in range(m, val - 1, -1):
            dp[j][s] += dp[j - 1][s - val]
            
print(dp[k][m])
        
