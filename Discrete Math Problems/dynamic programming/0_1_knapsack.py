
def knapsack(items, capacity):
    n = len(items)
    
    weights = [item[1] for item in items]
    profits = [item[0] for item in items]
    
    K = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):            
            if weights[i - 1] <= w:
                K[i][w] = max(K[i - 1][w], K[i - 1][w - weights[i - 1]] + profits[i - 1]) # DP table is offset by 1     
            else:
                K[i][w] = K[i - 1][w] 
                
    return K[n][capacity]
    


m = 8  # Capacity of the knapsack
items = [(1, 2), (2, 3), (5, 4), (6, 5)]  # (profit, weight)

print(knapsack(items, m))  # Expected output: 