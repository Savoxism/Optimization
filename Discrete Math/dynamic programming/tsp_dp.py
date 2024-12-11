from itertools import permutations 

def tsp(cost_matrix):
    n = len(cost_matrix)
    all_cities = set(range(n))
    
    # DP table: g[i][subset] stores minimum cost to visit subset starting at i
    dp = {}
    parent = {}
    
