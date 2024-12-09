import sys

# Read input
def read_input():
    n, K, Q = map(int, input().strip().split())  # Number of clients, trucks, capacity
    demands = list(map(int, input().strip().split()))  # Packages requested by clients
    distance_matrix = []
    for _ in range(n + 1):  # Read the distance matrix (including depot)
        distance_matrix.append(list(map(int, input().strip().split())))
    return n, K, Q, demands, distance_matrix

# Backtracking function
def solve():
    n, K, Q, demands, c = read_input()

    # Variables
    y = [-1] * K  # First delivery point for each truck
    x = [-1] * (n + 1)  # Next point for each point
    visited = [False] * (n + 1)  # Track if a client has been visited
    load = [0] * K  # Load of each truck
    f = 0  # Total length of the current solution
    best_distance = [sys.maxsize]  # Best distance found so far