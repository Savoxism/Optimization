import sys

'''
8 12 5 6
1 1 0 0 0 0 1 0 0 0 0 1
1 0 0 0 1 1 0 1 0 0 1 1
0 0 1 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 1 0 0 1 0 1
1 0 0 1 0 0 0 0 0 1 0 0
1 0 1 0 1 0 0 0 1 0 1 0 
0 0 0 0 1 0 1 0 0 0 0 0
1 0 1 1 0 1 1 1 0 1 0 1
'''

n, m, r, c = map(int, sys.stdin.readline().split())
A = [list(map(int, input().split())) for _ in range(n)]

r -= 1
c -= 1

visited = [[0] * m for _ in range(n)]
queue   = [[r, c, 0]]
visited[r][c] = 1

dx = [-1, 1, 0, 0]
dy = [0, 0, -1, 1]

found = -1
head  = 0

while head < len(queue):
    x, y, steps = queue[head]
    head += 1

    if x == 0 or x == n-1 or y == 0 or y == m-1:
        found = steps + 1
        break

    for i in range(4):
        nx = x + dx[i]
        ny = y + dy[i]
        if 0 <= nx < n and 0 <= ny < m:
            if A[nx][ny] == 0 and visited[nx][ny] == 0:
                visited[nx][ny] = 1
                queue.append([nx, ny, steps+1])

print(found)