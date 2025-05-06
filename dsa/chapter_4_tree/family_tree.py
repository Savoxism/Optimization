import sys
sys.setrecursionlimit(20000)

'''
Peter Newman
Michael Thomas
John David
Paul Mark
Stephan Mark
Pierre Thomas
Mark Newman
Bill David
David Newman
Thomas Mark
***
descendants Newman
descendants Mark
descendants David
generation Mark
***
'''

children = {}
for line in sys.stdin:
    relationship = line.strip()
    
    if relationship == "***":
        break
    
    child, parent = relationship.split()
    children.setdefault(parent, []).append(child)
    children.setdefault(child, [])


descendants = {}
def count_desc(name):
    if name in descendants:
        return descendants[name]
    
    count = 0
    for ch in children.get(name, []):
        count += 1 + count_desc(ch)
        
    descendants[name] = count
    return count

generations = {}
def max_gen(name):
    if name in generations:
        return generations[name]
    
    depth = 0
    for ch in children.get(name, []):
        depth = max(depth, max_gen(ch))
        
    res = depth + (1 if children.get(name) else 0)
    generations[name] = res
    return res

for line in sys.stdin:
    s = line.strip()
    if s == "***":
        break
    cmd, name = s.split()
    if cmd == "descendants":
        print(count_desc(name) if name in children else 0)
    else:  
        print(max_gen(name) if name in children else 0)
        pass