import sys

"""
5 8
1 2 1
1 3 4
1 5 1
2 4 2
2 5 1
3 4 3
3 5 3
4 5 2
"""

def input_data():
    input = sys.stdin.readline
    n, m = map(int, input().split())
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((u, v, w))
    return n, m, edges

class Union:
    def __init__(self, n):
        self.parent = list(range(n+1))
        self.rank = [0] * (n + 1)
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    def union(self, x, y):
        xr, yr = self.find(x), self.find(y)
        if xr == yr:
            return False
        if self.rank[xr] < self.rank[yr]:
            self.parent[xr] = yr
        else:
            self.parent[yr] = xr
            if self.rank[xr] == self.rank[yr]:
                self.rank[xr] += 1
        return True
    
def kruskal(n, edges):
    uf = Union(n)
    mst_weight = 0
    edge_cnt = 0
    edges.sort(key=lambda x: x[2])

    for u, v, w in edges:
        if uf.union(u, v):
            mst_weight += w
            edge_cnt += 1
            if edge_cnt == n - 1:
                break
    
    if edge_cnt < n - 1:
        print("ERROR: Graph G is not connected")
        return -1
    else:
        return mst_weight
    
n, m, edges = input_data()
cost = kruskal(n, edges=edges)
print(cost)