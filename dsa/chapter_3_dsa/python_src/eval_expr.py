import re

'''
(2+4*10)*(5) + 7

((2+4*10)*(5) + 7
'''

MOD = 10**9 + 7

s = input().strip()
stack = []
correct = True

for c in s:
    if c == "(":
        stack.append(c)
    elif c == ")":
        if not stack or stack[-1] != "(":
            correct = False
            break
        stack.pop()

if stack:
    correct = False
    
if not correct:
    print("NOT_CORRECT")
else:
    try:
        expr = re.sub(r'\s+', '', s)  
        if not re.fullmatch(r'[0-9+\-*()]*', expr):
            print("NOT_CORRECT")
        else:
            result = eval(expr)
            print(result % MOD)
    except:
        print("NOT_CORRECT")
