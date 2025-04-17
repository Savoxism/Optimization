class Node:
    def __init__(self, id):
        self.id = id
        self.first_child = None
        self.next_sibling = None
        
nodes = {}
root = None

def make_root(u):
    global root
    root = Node(u)
    nodes[u] = root
    
def insert(u, v):
    parent = nodes[v]
    new_node = Node(u)
    nodes[u] = new_node
    
    if not parent.first_child:
        parent.first_child = new_node
    else:
        child = parent.first_child
        while child.next_sibling:
            child = child.next_sibling
        child.next_sibling = new_node
        
def compute_height(node):
    if node is None:
        return -1
    
    if not node.first_child:
        return 0
    
    max_child_height = -1
    child = node.first_child
    while child:
        max_child_height = max(max_child_height, compute_height(child))
        child = child.next_sibling
    
    return max_child_height + 1

def main():
    while True:
        line = input().strip()
        if line == '*':
            break

        parts = line.split()
        cmd = parts[0]

        if cmd == 'MakeRoot' and len(parts) == 2:
            make_root(int(parts[1]))

        elif cmd == 'Insert' and len(parts) == 3:
            u, v = int(parts[1]), int(parts[2])
            insert(u, v)

        elif cmd == 'Height' and len(parts) == 2:
            u = int(parts[1])
            height = compute_height(nodes[u])
            print(f"Height of node {u}: {height}")
        
        else:
            print(f"Invalid command or missing arguments: {line}")

if __name__ == "__main__":
    main()