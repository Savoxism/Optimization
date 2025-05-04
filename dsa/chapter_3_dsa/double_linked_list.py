import sys

'''
5
5 4 3 2 1
addlast 3
addlast 10
addfirst 1
addafter 10 4
remove 1
output 0
#
'''

class Node:
    def __init__(self, data):
        self.data = data # the value of the node
        self.prev = None # last node on the left
        self.next = None # next node on the right
        
class DoublyLinkedList:
    def __init__(self):
        self.head = None # first node
        self.tail = None # last node
        
    def exists(self, value):
        current = self.head
        while current:
            if current.data == value:
                return True
            current = current.next
        return False
    
    def add_first(self, value):
        if self.exists(value): return 
        
        new_node = Node(value)
        if self.head is None:
            self.head = self.tail = new_node
        else:
            new_node.next = self.head # forward mapping
            self.head.prev = new_node # backward mapping
            self.head = new_node
            
    def add_last(self, value):
        if self.exists(value): return
        
        new_node = Node(value)
        # if the current list if empty 
        if self.tail is None:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
            
    def add_after(self, u, v): # [5] <-> [4] <-> [3]
        if self.exists(u): return
        
        current = self.head
        
        while current:
            if current.data == v:
                new_node = Node(u)
                new_node.prev = current
                new_node.next = current.next # point to the next element to the right
                
                if current.next:
                    current.next.prev = new_node
                else:
                    self.tail = new_node
                    
                current.next = new_node
                break
                
            current = current.next
            
    def add_before(self, u, v):
        if self.exists(u): return 
        
        current = self.head
        while current:
            if current.data == v:
                new_node = Node(u)
                new_node.next = current
                new_node.prev = current.prev
                
                if not current.prev:
                    self.head = new_node
                else:
                    current.prev.next = new_node
                    
                current.prev = new_node
                break
            current = current.next
            
    def remove(self, value):
        current= self.head
        
        while current:
            if current.data == value:
                
                # in-between element
                if current.prev:
                    current.prev.next = current.next
                else:
                    self.head = current.next
                    
                if current.next:
                    current.next.prev = current.prev
                else:
                    self.tail = current.prev
                
                break
            
            current = current.next
            
    def reverse(self):
        current = self.head
        while current:
            current.prev, current.next = current.next, current.prev
            current = current.prev
        
        self.head, self.tail = self.tail, self.head
            
    def output(self, direction):
        result = []
        if direction == 1:
            current = self.head
            while current:
                result.append(str(current.data))
                current = current.next
        
        else:
            current = self.tail
            while current:
                result.append(str(current.data))
                current = current.prev
        print(*result)
            
            
dll = DoublyLinkedList()

n = int(input())
initials = list(map(int, input().split()))
for val in initials:
    dll.add_last(val)

# operation center
while True:
    line = input()
    if line == "#":
        break
    parts = line.split()
    cmd = parts[0]

    if cmd == "addfirst":
        dll.add_first(int(parts[1]))
    elif cmd == "addlast":
        dll.add_last(int(parts[1]))
    elif cmd == "addafter":
        dll.add_after(int(parts[1]), int(parts[2]))
    elif cmd == "addbefore":
        dll.add_before(int(parts[1]), int(parts[2]))
    elif cmd == "remove":
        dll.remove(int(parts[1]))
    elif cmd == "reverse":
        dll.reverse()
    elif cmd == "output":
        dll.output(int(parts[1]))