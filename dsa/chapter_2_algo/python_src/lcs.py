

str1 = "KJCDEFG"
str2 = "CCEDEGF"

length1 = len(str1)
length2 = len(str2)

dp = [[0] * (length2 + 1) for _ in range(length1 + 1)]

for i in range(1, length1 + 1):
    for j in range(1, length2 + 1):
        if str1[i - 1] == str2[j - 1]:
            dp[i][j] = dp[i-1][j-1] + 1
        else:
            dp[i][j] = max(dp[i-1][j], dp[i][j-1])


# print(dp)

lcs = []
i, j = length1, length2

while i > 0 and j > 0:
    if str1[i-1] == str2[j-1]:
        lcs.append(str1[i-1])
        i -= 1
        j -= 1
    elif dp[i-1][j] > dp[i][j-1]:
        i -= 1
    else:
        j -= 1

lcs.reverse()

print(dp[length1][length2])

print(lcs)