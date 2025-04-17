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

def count_leaves(node):
    if not node:
        return 0
    if not node.first_child:
        return 1
    
    count = 0
    child = node.first_child
    while child:
        count += count_leaves(child)
        child = child.next_sibling
    return count

def count_k_children(node, k):
    if not node:
        return 0
    
    count = 0
    child = node.first_child
    while child:
        count += 1
        child = child.next_sibling

    result = 1 if count == k else 0

    child = node.first_child
    while child:
        result += count_k_children(child, k)
        child = child.next_sibling

    return result

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
            if v in nodes:
                insert(u, v)
            else:
                print(f"Error: parent node {v} not found.")

        elif cmd == 'CountLeaves' and len(parts) == 2:
            u = int(parts[1])
            if u in nodes:
                print(count_leaves(nodes[u]))
            else:
                print(f"Error: node {u} not found.")

        elif cmd == 'CountKChildren' and len(parts) == 3:
            u, k = int(parts[1]), int(parts[2])
            if u in nodes:
                print(count_k_children(nodes[u], k))
            else:
                print(f"Error: node {u} not found.")

        else:
            print(f"Invalid command or missing arguments: {line}")

if __name__ == "__main__":
    main()
