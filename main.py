
# x handler
def check_x(vertex,k):
    global Q
    global d

    if vertex > 0 and visited[vertex]:
        return False
    if load[k] + d[vertex] > Q:
        return False

    return True
        
def backtracking_x(state,k):
    global segments
    global nbR
    global Cmin
    global f
    global f_star
    global K
    global n
    
    
    #điều kiện dừng trường hợp riêng x
    if state == 0: # về depot đi cu
        if k < K:
            backtracking_x(y[k+1],k + 1) 
            # đi tìm tiếp cho xe k + 1 
        
        return 

    for vertex in range(0,n+1):
        if  state != vertex:
            if check_x(vertex,k):
                
                x[state] = vertex
                
                visited[vertex] = True
                f = f + matrix[state][vertex]
                load[k] += d[vertex]
                segments = segments + 1
                
                # logic backtrack_x
                
                if vertex > 0:
                    #real customer
                    if f + (n + nbR - segments)* Cmin < f_star:
                        backtracking_x(vertex,k)
                else:
                    if k == K:
                        if segments == n + nbR:
                            update_best()
                    else:
                        if f + (n + nbR - segments) * Cmin < f_star:
                                backtracking_x(y[k+1],k+1)
                
                # trả lại value
                
                visited[vertex] = False
                f -=  matrix[state][vertex]
                load[k] = load[k] - d[vertex]
                segments = segments - 1


# cập nhật ngon nhất
def update_best(): 
    global f_star
    global f
    
    if f  < f_star:
        
        f_star = f 
# y handler

def check_y(vertex,k):

    global Q
    global d
    
    if vertex == 0:
        return True
    if load[k] + d[vertex] > Q:
        return False
    if visited[vertex] == True:
        return False
    
    return True

#k là xe thứ k hiện tại
def backtracking_y(k):
    global segments
    global nbR
    global Cmin
    global f
    global f_star
    global K
    global n

    s = 0
    if y[k-1] > 0:
        s = y[k-1] + 1
    
    for vertex in range(s,n+1):
        if check_y(vertex,k):
            y[k] = vertex
            if vertex > 0:
                segments = segments + 1
            
            visited[vertex] = True
            f = f + matrix[0][vertex]
            load[k] = load[k] + d[vertex]
            
            if k < K:
                backtracking_y(k + 1)
            else:
                nbR = segments
                backtracking_x(y[1],1)
            
            
            # trả lại giá trị
            if vertex > 0:
                segments = segments - 1
            
            
            load[k] = load[k] - d[vertex]
            visited[vertex] = False
            f = f - matrix[0][vertex]
           

              
# solve handler 
#input handler
n,K,Q = (int(x) for x in input().split())
d = [0] + [int (x) for x in input().split()]
matrix = []
for i in range(n + 1):
    matrix.append([int(x) for x in input().split()])

#logic variable handler

x = [None] + [0 for i in range(n)]
y = [None] + [0  for i in range(K)]


load = [None] + [0 for i in range(K)]
nbR = 0
segments = 0
# k = 1

# tính Cmin
Cmin = 10000
for i in range(0,n + 1):
    for j in range(0,n + 1):
        if i != j:
            Cmin = min(Cmin,matrix[i][j])
Cmin += 0.95
f = 0
f_star = 10000

y[0] = 0
visited = [False]+[False for i in range(n)]

backtracking_y(1)
print(f_star)
