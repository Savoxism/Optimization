from collections import defaultdict
import heapq
import sys 

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
    min_heap = [(0, 0, -1)]  # (cost, current_node, parent)

    while min_heap:
        cost, current, parent = heapq.heappop(min_heap)
        if visited[current]:
            continue
        visited[current] = True
        if parent != -1:
            mst[parent].append(current)
            mst[current].append(parent)
        for neighbor in range(n):
            if not visited[neighbor]:
                heapq.heappush(min_heap, (cost_matrix[current][neighbor], neighbor, current))
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

def compute_one_tree(n, cost_matrix, excluded_node):
    reduced_cost_matrix = [row[:excluded_node] + row[excluded_node + 1:] for i, row in enumerate(cost_matrix) if i != excluded_node]
    reduced_n = n - 1

    mst = compute_mst(reduced_n, reduced_cost_matrix)

    node_map = list(range(n))
    node_map.pop(excluded_node)

    full_mst = defaultdict(list)
    for i in range(reduced_n):
        for j in mst[i]:
            full_mst[node_map[i]].append(node_map[j])

    min_edges = sorted([(cost_matrix[excluded_node][i], i) for i in range(n) if i != excluded_node])[:2]

    full_mst[excluded_node] = [min_edges[0][1], min_edges[1][1]]
    full_mst[min_edges[0][1]].append(excluded_node)
    full_mst[min_edges[1][1]].append(excluded_node)

    one_tree_cost = 0
    visited_edges = set()
    for i in full_mst:
        for j in full_mst[i]:
            if (i, j) not in visited_edges and (j, i) not in visited_edges:
                one_tree_cost += cost_matrix[i][j]
                visited_edges.add((i, j))

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

    # Step 1: Generate heuristic solution
    heuristic_cost = generate_heuristic_solution(n, cost_matrix)

    # Step 2: Compute lower bound using one-trees
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