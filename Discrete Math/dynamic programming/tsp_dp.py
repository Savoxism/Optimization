
def tsp_dp(cost_matrix):
    n = len(cost_matrix) 
    dp = {}  

    def g(current_city, remaining_set):
        state = (current_city, frozenset(remaining_set))

        if state in dp:
            return dp[state]

        # Base case
        if not remaining_set:
            dp[state] = cost_matrix[current_city][0] 
            return dp[state]

        # Recursive cas - Compute g(i, S) = min_k { c(i, k) + g(k, S - {k}) }
        min_cost = float('inf')
        for next_city in remaining_set:
            next_set = remaining_set - {next_city}
            cost = cost_matrix[current_city][next_city] + g(next_city, next_set)
            min_cost = min(min_cost, cost)

        dp[state] = min_cost  
        return min_cost

    
    full_set = set(range(1, n)) 
    min_cost = g(0, full_set)
    
    # Path reconstruction
    path = [0]
    remaining_set = full_set
    current_city = 0

    while remaining_set:
        next_city = None
        best_cost = float('inf')

        # Find the next city that minimizes the cost
        for candidate_city in remaining_set:
            next_set = remaining_set - {candidate_city}
            state = (candidate_city, frozenset(next_set))
            cost = cost_matrix[current_city][candidate_city] + dp[state]
            if cost < best_cost:
                best_cost = cost
                next_city = candidate_city

        path.append(next_city)
        remaining_set = remaining_set - {next_city}
        current_city = next_city

    path.append(0) 
    
    return min_cost, path


# Input cost matrix
cost_matrix = [
    [0, 10, 15, 20],
    [5,  0,  9, 10],
    [6, 13,  0, 12],
    [8,  8,  9,  0]
]

min_cost, path = tsp_dp(cost_matrix)
print("Minimum Cost:", min_cost)
print("Optimal Path:", path)
