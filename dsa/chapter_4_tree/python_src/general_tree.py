import sys
sys.setrecursionlimit(1000000)

'''
MakeRoot 10
Insert 11 10
Insert 1 10
Insert 3 10
Insert 5 11
Insert 4 11
Height 10
Depth 10
Insert 8 3
Insert 2 3
Insert 7 3
Insert 6 4
Insert 9 4
Height 10
Depth 10
Depth 3
*
'''

children = {} # id -> list of children
parent = {} # id -> id of parent
root = None

def compute_height(u):
    if not children[u]: # leave
        return 1
    
    h = 0
    for v in children[u]:
        h = max(h, compute_height(v))
    return h + 1

for line in sys.stdin:
    line = line.strip()
    if line == "*":
        break
    
    parts = line.split()
    cmd = parts[0]
    
    if cmd == "MakeRoot":
        u = int(parts[1])
        root = u
        children[u] = []
        parent[u] = None
    
    elif cmd == "Insert":
        u, v = map(int, parts[1: ])
        
        if v in children and u not in children: 
            children[v].append(u)
            children[u] = []
            parent[u] = v
            
    elif cmd == "Height":
        u = int(parts[1])
        print(compute_height(u) if u in children else 0)
        
    elif cmd == "Depth":
        u = int(parts[1])
        
        d = 0
        cur = u if u in children else None
        
        while cur is not None:
            d += 1
            cur = parent[cur]
        print(d)