from collections import defaultdict
from heapq import heappop, heappush
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
    '''
    n: number of nodes
    m: number of edges
    k; number of forbidden pairs
    s: source node
    t: target node
    '''
    input = sys.stdin.read()
    lines = input.split('\n')
    n, m, k, s, t = map(int, lines[0].split())
    
    edges = []
    for i in range(m):
        u, v, cost = map(int, lines[i+1].split())
        
        edges.append((u, v, cost))
        
    forbidden_pairs = []
    for i in range(k):
        e1_start, e1_end, e2_start, e2_end = map(int, lines[m+i+1].split())
        
        forbidden_pairs.append((e1_start, e1_end, e2_start, e2_end))
        
    return n, m, k, s, t, edges, forbidden_pairs

def solve(n, m, k, s, t, edges, forbidden_pairs):
    graph = defaultdict(list)
    forbidden_set = set()
    
    # Add edges to graph
    for u, v, cost in edges:
        graph[u].append((v, cost))
        
    # Add forbidden pairs to set
    for e1_start, e1_end, e2_start, e2_end in forbidden_pairs:
        forbidden_set.add(((e1_start, e1_end), (e2_start, e2_end)))
        forbidden_set.add(((e2_start, e2_end), (e1_start, e1_end)))
        
    pq = [(0, s, None)] # (cost, current_edge, last_edge)
    visited = set()      

    while pq:
        cost, current, last_edge = heappop(pq)
        
        if current == t:
            return cost
        
        if (current, last_edge) in visited:
            continue
        
        visited.add((current, last_edge))
        
        for neighbor, edge_cost in graph[current]:
            current_edge = (current, neighbor)
            
            # 1) If there is a previous edge 2) if the pair (last_edge, current_edge) is in the forbidden set
            if last_edge and ((last_edge, current_edge) in forbidden_set):
                continue
            
            heappush(pq, (cost + edge_cost, neighbor, current_edge))

    return -1

m, n , k, s, t, edges, forbidden_pairs = read_input()

print(solve(n, m, k, s, t, edges, forbidden_pairs))