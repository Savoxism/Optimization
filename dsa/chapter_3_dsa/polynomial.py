import sys

'''
AddTerm 1 3 2
AddTerm 1 4 0
AddTerm 1 6 2
AddTerm 2 3 2
AddTerm 2 7 5
PrintPoly 1
PrintPoly 2
AddPoly 2 1 3
PrintPoly 3
EvaluatePoly 2 1
*
'''
class TermNode:
    def __init__(self, coef: int, exp: int):
        self.coef = coef
        self.exp = exp
        self.next = None
        
polys = {} # dict[int, TermNode]

def create_poly(pid: int):
    if pid not in polys:
        polys[pid] = None
        
def add_term(pid: int, coef: int, exp: int):
    if pid not in polys:
        polys[pid] = None
        
    head = polys[pid]
    prev = None
    curr = head
    
    while curr and curr.exp > exp:
        prev, curr = curr, curr.next
    
    if curr and curr.exp == exp:
        curr.coef += coef
        if curr.coef == 0:
            if prev:
                prev.next = curr.next
            else:
                polys[pid] = curr.next
                
    else:
        new_node = TermNode(coef, exp)
        new_node.next = curr
        if prev:
            prev.next = new_node
        else:
            polys[pid] = new_node
            
def print_poly(pid: int):
    head = polys.get(pid)
    if not head:
        print(0)
        return
    out = []
    curr = head
    while curr:
        out.append(f"{curr.coef} {curr.exp}")
        curr = curr.next
    print(" ".join(out))

def eval_poly(pid: int, v: int):
    head = polys.get(pid)
    if not head:
        print(0)
        return
    res = 0
    curr = head
    while curr:
        res += curr.coef * (v ** curr.exp)
        curr = curr.next
    print(res)

def add_poly(pid1: int, pid2: int, result_pid: int):
    polys[result_pid] = None

    for src in (pid1, pid2):
        curr = polys.get(src)
        while curr:
            add_term(result_pid, curr.coef, curr.exp)
            curr = curr.next

def destroy_poly(pid: int):
    if pid in polys:
        del polys[pid]

import sys

for line in sys.stdin:
    line = line.strip()
    if not line or line == "*":
        break
    parts = line.split()
    cmd = parts[0]

    if cmd == "Create":
        pid = int(parts[1])
        create_poly(pid)

    elif cmd == "AddTerm":
        pid, coef, exp = map(int, parts[1:])
        add_term(pid, coef, exp)

    elif cmd == "PrintPoly":
        pid = int(parts[1])
        print_poly(pid)

    elif cmd == "EvaluatePoly":
        pid, v = map(int, parts[1:])
        eval_poly(pid, v)

    elif cmd == "AddPoly":
        pid1, pid2, res = map(int, parts[1:])
        add_poly(pid1, pid2, res)

    elif cmd == "Destroy":
        pid = int(parts[1])
        destroy_poly(pid)
