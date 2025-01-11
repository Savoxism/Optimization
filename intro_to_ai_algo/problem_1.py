import sys
"""
6 10 3 3 
1 2 1
1 3 2
1 5 3
2 4 8
2 5 5 
2 6 9
3 4 7
3 5 4
4 5 6 
4 6 10
"""

def read_input():
    input = sys.stdin.read().splitlines()
    n_m_D_K = input[0].split()
    n = int(n_m_D_K[0])
    m = int(n_m_D_K[1])
    D = int(n_m_D_K[2])
    K = int(n_m_D_K[3])
    
    egdes = []
    for i in range(1, m + 1):
        u_v_w = input[i].split()
        u = int(u_v_w[0])
        v = int(u_v_w[1])
        w = int(u_v_w[2])
        egdes.append((u, v, w))
        
    return n, m, D, K, egdes

def solve(n, m, D, K, edges):
    edges.sort(key=lambda x: x[2])
    
    degree = [0] * (n + 1)
    
    selected_edges = []
    total_weight = 0
    
    for u, v, w in edges:
        # Check if adding this edge violates the degree constraint
        if degree[u] <= D and degree[v] <= D:
            selected_edges.append((u, v))
            total_weight += w
            degree[u] += 1
            degree[v] += 1
            
            # Stop if we have selected K edges
            if len(selected_edges) == K:
                break
            
    if len(selected_edges) == K:
        print(total_weight)
        for u, v in selected_edges:
            print(u, v)
    else:
        print("NOT_FEASIBLE")
        
        
if __name__ == "__main__":
    n, m, D, K, edges = read_input()
    
    solve(n, m, D, K, edges)
    
    