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
    
edges = [(1, 2), (2, 3), (3, 4)]
u = Union(4)
for a, b in edges:
    if u.find(a) != u.find(b):
        u.union(a, b)
        print(True)
