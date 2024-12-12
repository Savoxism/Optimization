from collections import defaultdict
import sys
 
'''
Assumption 1: Symmetric TSP
Assumption 2: Triangle Inequality holds
'''

def read_input():
    n = int(sys.stdin.readline().strip())
    cost_matrix = []
    for _ in range(n):
        row = [int(x) for x in sys.stdin.readline().split()]
        cost_matrix.append(row)
    return n, cost_matrix

def compute_mst(n, cost_matrix):
    mst = defaultdict(list)
    visited = [False] * n
    priority_queue = [(0, 0, -1)] # (cost, node, parent)
    
    while priority_queue:
        priority_queue.sort(key=lambda x: x[0])
        cost, current, parent = priority_queue.pop(0)
        
        if visited[current]:
            continue
        
        visited[current] = True
        
        if parent != -1:
            mst[parent].append(current)
            mst[current].append(parent)
            
        for neighbor in range(n):
            if not visited[neighbor]:
                priority_queue.append((cost_matrix[current][neighbor], neighbor, current))        
    return mst

def preorder_traversal(mst, start):
    tour = []
    visited = set()
    def dfs(node):
        if node in visited:
            return
        visited.add(node)
        tour.append(node)
        for neighbor in mst[node]:
            dfs(neighbor)
    dfs(start)
    return tour

def generate_heuristic_solution(n, cost_matrix):
    mst = compute_mst(n, cost_matrix)

    # Find two nodes with degree 1
    degree = defaultdict(int)
    for node in mst:
        degree[node] += len(mst[node])

    nodes_with_degree_one = [node for node in degree if degree[node] == 1]

    if len(nodes_with_degree_one) == 2:
        mst[nodes_with_degree_one[0]].append(nodes_with_degree_one[1])
        mst[nodes_with_degree_one[1]].append(nodes_with_degree_one[0])

    tour = preorder_traversal(mst, 0)
    tour.append(0)

    total_cost = 0
    for i in range(len(tour) - 1):
        total_cost += cost_matrix[tour[i]][tour[i + 1]]

    return total_cost

def compute_one_tree(num_nodes, cost_matrix, excluded_node):
    # Reduce the cost matrix to exclude the specified node
    reduced_cost_matrix = [
        row[:excluded_node] + row[excluded_node + 1:]
        for i, row in enumerate(cost_matrix) if i != excluded_node
    ]
    reduced_num_nodes = num_nodes - 1

    # Compute the MST on the reduced cost matrix
    mst = compute_mst(reduced_num_nodes, reduced_cost_matrix)

    # Map the reduced node indices back to the original indices
    node_mapping = list(range(num_nodes))
    node_mapping.pop(excluded_node)

    one_tree = defaultdict(list)
    for reduced_node in range(reduced_num_nodes):
        for connected_node in mst[reduced_node]:
            one_tree[node_mapping[reduced_node]].append(node_mapping[connected_node])

    # Find the two smallest edges connecting the excluded node
    smallest_edges = sorted([
        (cost_matrix[excluded_node][neighbor], neighbor)
        for neighbor in range(num_nodes) if neighbor != excluded_node
    ])[:2]

    # Add the excluded node and its connections to the one-tree
    one_tree[excluded_node] = [smallest_edges[0][1], smallest_edges[1][1]]
    one_tree[smallest_edges[0][1]].append(excluded_node)
    one_tree[smallest_edges[1][1]].append(excluded_node)

    # Calculate the total cost of the one-tree
    one_tree_cost = 0
    visited_edges = set()
    for node in one_tree:
        for connected_node in one_tree[node]:
            if (node, connected_node) not in visited_edges and (connected_node, node) not in visited_edges:
                one_tree_cost += cost_matrix[node][connected_node]
                visited_edges.add((node, connected_node))

    return one_tree_cost

def compute_lower_bound(n, cost_matrix):
    best_one_tree_cost = float('-inf')
    for excluded_node in range(n):
        one_tree_cost = compute_one_tree(n, cost_matrix, excluded_node)
        best_one_tree_cost = max(best_one_tree_cost, one_tree_cost)
    return best_one_tree_cost

def compare_with_optimal_solution(n, cost_matrix):
    from itertools import permutations

    optimal_cost = float('inf')
    for perm in permutations(range(n)):
        cost = 0
        for i in range(n):
            cost += cost_matrix[perm[i]][perm[(i + 1) % n]]
        optimal_cost = min(optimal_cost, cost)

    return optimal_cost

def main():
    n, cost_matrix = read_input()

    heuristic_cost = generate_heuristic_solution(n, cost_matrix)

    lower_bound = compute_lower_bound(n, cost_matrix)

    # Step 3: Compare heuristic solution with optimal solution (if feasible)
    if n <= 10:
        optimal_cost = compare_with_optimal_solution(n, cost_matrix)
        print("Heuristic Cost:", heuristic_cost)
        print("Lower Bound:", lower_bound)
        print("Optimal Cost:", optimal_cost)
    else:
        print("Heuristic Cost:", heuristic_cost)
        print("Lower Bound:", lower_bound)

if __name__ == "__main__":
    main()