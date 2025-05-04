import sys

'''
5
5 4 3 2 1
addlast 3
addlast 10
addfirst 1
addafter 10 4
remove 1
#
'''

n = map(int, sys.stdin.readline())

linked_list = list(map(int, sys.stdin.readline().split()))

while True:
    cmd = input()
    
    if cmd == "#":
        break
    
    parts = cmd.split()
    op = parts[0]
    
    if op == "addlast":
        k = int(parts[1])
        if k not in linked_list:
            linked_list.append(k)
        
    elif op == "addfirst":
        k = int(parts[1])
        if k not in linked_list:
            linked_list.insert(0, k)
        
    elif op == "addafter":
        u = int(parts[1])
        v = int(parts[2])
        
        if v in linked_list and u not in linked_list:
            idx = linked_list.index(v)
            linked_list.insert(idx + 1, u)
        
    elif op == "addbefore":
        u = int(parts[1])
        v = int(parts[2])
        
        if v in linked_list and u not in linked_list:
            idx = linked_list.index(v)
            linked_list.insert(idx, u)
        
    elif op == "remove":
        k = int(parts[1])
        if k in linked_list:
            linked_list.remove(k)
        
    elif op == "reverse":
        linked_list = linked_list[::-1]
             
print(*linked_list)