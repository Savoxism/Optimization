import sys
from collections import defaultdict

'''
Assumption 1: The cost matrix is symmetric.
Assumption 2: The triangle inequality holds.
'''

def read_input():
    n = int(sys.stdin.readline().strip())
    cost_matrix = []
    
    for _ in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        cost_matrix.append(row)
        
    return n, cost_matrix

def compute_mst(cost_matrix):
    num_nodes = len(cost_matrix)
    mst = defaultdict(list) 
    
    visited = [False] * num_nodes
    
    # Priority queue to store edges in the format (cost, from_node, to_node)
    edges = []
    for to_node in range(1, num_nodes):
        edges.append((cost_matrix[0][to_node], 0, to_node)) # init with node 0
        
    visited[0] = True
    mst_cost = 0
    
    while edges:
        edges.sort(key=lambda x: x[0])
        cost, from_node, to_node = edges.pop(0)
        
        if visited[to_node]:
            continue
        
        mst[from_node].append(to_node)
        mst[to_node].append(from_node) # undirected graph
        mst_cost += cost
        
        visited[to_node] = True
        for next_node in range(num_nodes):
            if not visited[next_node]:
                edges.append((cost_matrix[to_node][next_node], to_node, next_node))
    
    return mst, mst_cost
    
def find_odd_degree_vertices(mst):
    odd_nodes = []
    for node, neighbors in mst.items():
        if len(neighbors) % 2 == 1:
            odd_nodes.append(node)
    return odd_nodes

def minimum_weight_perfect_matching(odd_vertices, cost_matrix):
    # Greedy method
    matching = []
    remaining = set(odd_vertices)
    
    while remaining:
        u = remaining.pop()
        min_cost = float('inf')
        best_match = None
        
        for v in remaining:
            if cost_matrix[u][v] < min_cost:
                min_cost = cost_matrix[u][v]
                best_match = v
                
        remaining.remove(best_match)
        matching.append((u, best_match))
        
    return matching

def combine_into_multigraph(mst, matching):
    multigraph = defaultdict(list)
    
    for u, neighbors in mst.items():
        for v in neighbors:
            multigraph[u].append(v)
            
    # Add matching edges to the multigraph
    for u, v in matching:
        multigraph[u].append(v)
        multigraph[v].append(u)

    return dict(multigraph)


def generate_eulerian_tour(multigraph, start_node):
    stack = [start_node]
    tour = []
    local_graph = {u: neighbors[:] for u, neighbors in multigraph.items()}

    while stack:
        node = stack[-1]
        if local_graph[node]:
            next_node = local_graph[node].pop()
            local_graph[next_node].remove(node)
            stack.append(next_node)
        else:
            tour.append(stack.pop())

    return tour[::-1]

def generate_tsp_tour(eulerian_tour, cost_matrix):
    tsp_tour = []
    visited = set()
    total_cost = 0

    prev_node = None
    for node in eulerian_tour:
        if node not in visited:
            tsp_tour.append(node)
            visited.add(node)
            if prev_node is not None:
                print(f"From city {prev_node} to city {node} with cost {cost_matrix[prev_node][node]}")
                total_cost += cost_matrix[prev_node][node]
            prev_node = node

    # Add cost to return to the starting node
    if tsp_tour:
        print(f"From city {tsp_tour[-1]} to city {tsp_tour[0]} with cost {cost_matrix[tsp_tour[-1]][tsp_tour[0]]}")
        total_cost += cost_matrix[tsp_tour[-1]][tsp_tour[0]]

    return tsp_tour, total_cost

def solve_tsp():
    n, cost_matrix = read_input()
    mst, mst_cost = compute_mst(cost_matrix)
    odd_degree_vertices = find_odd_degree_vertices(mst)
    matching = minimum_weight_perfect_matching(odd_degree_vertices, cost_matrix)
    multigraph = combine_into_multigraph(mst, matching)
    eulerian_tour = generate_eulerian_tour(multigraph, 0)
    tsp_tour, tsp_cost = generate_tsp_tour(eulerian_tour, cost_matrix)
    
    return tsp_cost, tsp_tour

if __name__ == '__main__':
    tsp_cost, tsp_tour = solve_tsp()
    print(tsp_cost)
    print(' '.join(str(x) for x in tsp_tour))





