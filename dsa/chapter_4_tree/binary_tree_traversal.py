import sys

class Node:
    def __init__(self, id):
        self.id = id
        self.left = None
        self.right = None
        
nodes = {} # id -> Node
root = None

for line in sys.stdin:
    line = line.strip()
    if line == "*":
        break
    
    parts = line.split()
    cmd = parts[0]
    
    if cmd == "MakeRoot":
        u = int(parts[1])
        root = Node(u)
        nodes[u] = root
        
    elif cmd == "AddLeft":
        u, v = int(parts[1]), int(parts[2])
        if u not in nodes and v in nodes:
            parent = nodes[v]
            if parent.left is None:
                node = Node(u)
                parent.left = node
                nodes[u] = node
                
    elif cmd == "AddRight":
        u, v = int(parts[1]), int(parts[2])
        if u not in nodes and v in nodes:
            parent = nodes[v]
            if parent.right is None:
                node = Node(u)
                parent.right = node
                nodes[u] = node
    else:
        res = []
        def preorder(n):
            if not n: return
            res.append(str(n.id))
            preorder(n.left)
            preorder(n.right)
        
        def inorder(n):
            if not n: return
            inorder(n.left)
            res.append(str(n.id))
            inorder(n.right)
            
        def postorder(n):
            if not n: return
            postorder(n.left)
            postorder(n.right)
            res.append(str(n.id))
            
        if cmd == "PreOrder":
            preorder(root)
            
        elif cmd == "InOrder":
            inorder(root)
        elif cmd == "PostOrder":
            postorder(root)
        else:
            print("Invalid command.")
        print(' '.join(res))
            