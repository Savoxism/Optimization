import sys

"""
MakeRoot 1
AddLeft 2 1
AddRight 3 1
AddLeft 9 2
AddRight 4 2
AddLeft 6 3
AddRight 5 3
AddLeft 7 4
AddRight 8 4
*
"""

class Node:
    def __init__(self, id):
        self.id = id
        self.left = None
        self.right = None

nodes = {}   
root = None

for line in sys.stdin:
    s = line.strip()
    if s == '*':
        break
    
    parts = s.split()
    cmd = parts[0]
    
    if cmd == 'MakeRoot':
        u = int(parts[1])
        root = Node(u)
        nodes[u] = root
        
    elif cmd == 'AddLeft':
        u, v = map(int, parts[1:])
        if u not in nodes and v in nodes:
            n = Node(u)
            nodes[u] = n
            nodes[v].left = n
            
    elif cmd == 'AddRight':
        u, v = map(int, parts[1:])
        if u not in nodes and v in nodes:
            n = Node(u)
            nodes[u] = n
            nodes[v].right = n

height_cache = {}

def compute_height(node: object) -> int:
    if node is None: # leaves
        return 0
    
    if node in height_cache:
        return height_cache[node]
    
    hL = compute_height(node.left)
    hR = compute_height(node.right)
    
    h = 1 + max(hL, hR)
    height_cache[node] = h
    return h

def is_balanced(node: object) -> bool:
    if node is None: return True
    
    hL = compute_height(node.left)
    hR = compute_height(node.right)
    
    if abs(hL - hR) > 1:
        return False
    
    return is_balanced(node.left) and is_balanced(node.right)

tree_h = compute_height(root)
is_tree_balanced = 1 if is_balanced(root) else 0

print(is_tree_balanced, tree_h)