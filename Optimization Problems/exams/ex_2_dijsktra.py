import sys

'''
7 18 2 1 0
2 1 115
6 5 175
6 2 200
4 3 149
6 1 155
5 6 179
0 4 125
4 1 124
2 3 155
5 4 107
4 2 172
6 4 175
4 6 103
1 6 121
3 2 132
3 6 103
4 0 197
2 0 138
2 1 0 4
5 6 4 3
'''

def read_input():
    lines = sys.stdin.readlines()

    n, m, k, s, t = map(int, lines[0].split())
    
    edges = []
    for i in range(1, m + 1):
        u, v, w = map(int, lines[i].split())
        edges.append((u, v, w))
    
    forbidden_pairs = []
    for i in range(m + 1, m + 1 + k):
        parts = lines[i].strip().split()
        start1, end1, start2, end2 = map(int, parts)
        forbidden_pairs.append(((start1, end1), (start2, end2))) 
        
    return n, m, k, s, t, edges, forbidden_pairs


def solve_dijsktra(n, m, s, t, edges, forbidden_pairs):
    adj_list = {u: [] for u in range(n)}
    for idx, (u, v, w) in enumerate(edges):
        adj_list[u].append((v, w, idx))
        
        
    forbidden_edge_indices = set()
    edge_to_index = {(u, v): idx for idx, (u, v, _) in enumerate(edges)}
    for pair in forbidden_pairs:
        edge1, edge2 = pair
        idx1 = edge_to_index.get(edge1, -1)
        idx2 = edge_to_index.get(edge2, -1)
        if idx1 != -1 and idx2 != -1:
            forbidden_edge_indices.add((idx1, idx2))
            
    INF = int(1e9)
    distances = {}  # (node, last_edge_index) -> distance
    for u in range(n):
        for edge_idx in range(-1, len(edges)):
            distances[(u, edge_idx)] = INF
    distances[(s, -1)] = 0  
    
    while True:
        min_dist = INF
        current_node = -1
        last_edge = -1
        
        for (u, edge), dist in distances.items():
            if dist < min_dist:
                min_dist = dist
                current_node = u
                last_edge = edge
                
        if min_dist == INF:
            break
        
        distances[(current_node, last_edge)] = INF
        
        if current_node == t:
            return float(min_dist)
        
        for v, w, edge_idx in adj_list[current_node]:
            forbidden = False
            for forbidden_pair in forbidden_edge_indices:
                if last_edge == forbidden_pair[0] and edge_idx == forbidden_pair[1]:
                    forbidden = True
                    break
            if not forbidden:
                # Relax the edge
                new_dist = min_dist + w
                if new_dist < distances[(v, edge_idx)]:
                    distances[(v, edge_idx)] = new_dist
    return -1

n, m, k, s, t, edges, forbidden_pairs = read_input()
cost = solve_dijsktra(n, m, s, t, edges, forbidden_pairs)
print(cost)
