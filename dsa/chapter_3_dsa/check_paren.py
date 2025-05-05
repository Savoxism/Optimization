
'''
(()[][]{}){}{}[][]({[]()})
'''

s = input().strip()

stack = []
bracket_map = {
    ')': '(',
    ']': '[',
    '}': '{',
}

valid = 1

for c in s:
    if c in "([{":
        stack.append(c)
    elif c in ")]}":
        if not stack or stack[-1] != bracket_map[c]:
            valid = 0
            break
        stack.pop()
    
if stack:
    valid = 0
    
print(valid)