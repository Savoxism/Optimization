class Node:
    def __init__(self, level, profit, weight, bound, u, c):
        self.level = level  
        self.profit = profit  
        self.weight = weight  
        self.bound = bound  
        self.u = u  
        self.c = c  

    def __lt__(self, other):
        return self.bound > other.bound

def calculate_bound_and_fractional(node, n, capacity, profits, weights):
    if node.weight >= capacity:
        return node.profit, node.profit, 0 

    u = node.profit 
    c = node.profit  
    total_weight = node.weight
    j = node.level + 1
    
    # Add full items when possible
    while j < n and total_weight + weights[j] <= capacity:
        total_weight += weights[j]
        u += profits[j]
        c += profits[j]
        j += 1
        
    if j < n:
        fraction = (capacity - total_weight) / weights[j] * profits[j]
        c += fraction
        
    return u, c, u

def knapsack_branch_and_bound(profits, weights, capacity):
    n = len(profits)
    
    queue = []
    
    # Initialize the queue with the root node
    initial_node = Node(-1, 0, 0, 0, 0, 0)
    u, c, bound = calculate_bound_and_fractional(initial_node, n, capacity, profits, weights)
    initial_node = Node(-1, 0, 0, bound, u, c)
    queue.append(initial_node)
    
    max_profit = 0
    
    while queue:
        current_node = max(queue, key=lambda x: x.bound) # highest bound
        queue.remove(current_node)
        
        # If this node cannot improve the max profit, skip it
        if current_node.bound <= max_profit:
            continue
        
        # Two cases: include the next item or not
        for include in [True, False]:
            next_level = current_node.level + 1
            
            # If we exceed the number of items, skip
            if next_level >= n:
                continue
            
            # Compute new profit and weight for this child node
            new_profit = current_node.profit + (profits[next_level] if include else 0)
            new_weight = current_node.weight + (weights[next_level] if include else 0)

            # If this node is feasible, calculate its bound and fractional profit
            if new_weight <= capacity:
                u, c, bound = calculate_bound_and_fractional(Node(next_level, new_profit, new_weight, 0, 0, 0), n, capacity, profits, weights)

                # Update max profit and add the node to the queue if its bound is promising
                if c > max_profit:
                    max_profit = c

                if bound > max_profit:
                    queue.append(Node(next_level, new_profit, new_weight, bound, u, c))

    return max_profit

# Example input
profits = [10, 10, 12, 18]  # Items are assumed sorted by profit/weight ratio
weights = [2, 4, 6, 9]
m = 15  # Capacity of the knapsack

result = knapsack_branch_and_bound(profits, weights, m)
print("Maximum profit (Branch and Bound):", result)