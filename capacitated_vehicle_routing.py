
def check_y(vertex, k):
    # depot
    if vertex == 0:
        return True
    # check if the load is over the capacity
    if load[k] + d[vertex] > Q:
        return False
    # if already visited
    if visited[vertex]:
        return False
    return True

def backtracking_y(k):
    global segments, nbR, f, f_star
    
    s = 0 if y[k - 1] == 0 else y[k - 1] + 1
    
    for vertex in range(s, n + 1):
        if check_y(vertex, k):
            y[k] = vertex
            
            # not depot
            if vertex > 0:
                segments += 1
                
            visited[vertex] = True
            f += dist_matrix[0][vertex]
            load[k] += d[vertex]
            
            # If there are still trucks to be assigned
            if k < K:
                backtracking_y(k + 1)
            else:
                nbR = segments
                backtracking_x(y[1], 1)
                
            # Backtrack
            if vertex > 0:
                segments -= 1
                
            load[k] = load[k] - d[vertex]
            visited[vertex] = False
            f = f - dist_matrix[0][vertex]

def check_x(vertex, k):
    if vertex > 0 and visited[vertex]:
        return False
    if load[k] + d[vertex] > Q:
        return False
    return True

def backtracking_x(state, k):
    global segments, nbR, f, f_star
    
    # If the state is 0, it means that the truck is returning to the depot
    if state == 0:
        # Check whether all customers have been visited
        if k < K:
            backtracking_x(y[k + 1], k + 1)
        return
    
    for vertex in range(0, n + 1):
        if state != vertex and check_x(vertex, k):
            x[state] = vertex
            visited[vertex] = True
            f += dist_matrix[state][vertex]
            load[k] += d[vertex]
            segments += 1
            
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
            f -=  dist_matrix[state][vertex]
            load[k] = load[k] - d[vertex]
            segments = segments - 1
            
            
def update_best():
    global f_star, f
    if f < f_star:
        f_star = f
        
        
n, K, Q = (int(x) for x in input().split())
d = [0] + [int (x) for x in input().split()]
dist_matrix = []
for i in range(n + 1):
    dist_matrix.append([int(x) for x in input().split()])

x = [None] + [0 for i in range(n)]
y = [None] + [0  for i in range(K)]
load = [None] + [0 for i in range(K)]
nbR = 0
segments = 0
visited = [False]+[False for i in range(n)]
f = 0
f_star = float('inf')

Cmin = min(
    dist_matrix[i][j]
    for i in range(n + 1)
    for j in range(n + 1)
    if i != j
)

y[0] = 0
backtracking_y(1)
print(f_star)