def fractional_knapsack(items, capacity):
    """_summary_
    Args:
        items (list): list of tuples where tuple (value, weight)
        capacity (int): maximum weight the knapsack can hold
    """
    # Value to weight ratio
    items = sorted(items, key=lambda x: x[0] / x[1], reverse=True)
    
    total_value = 0.0
    remaining_capacity = capacity
    selected_items = [] 
    
    for value, weight in items:
        if weight <= remaining_capacity:
            # Take the whole item
            total_value += value
            remaining_capacity -= weight
            selected_items.append((value, weight, 1.0))
        else:
            # Take a fraction of the item
            fraction = remaining_capacity / weight
            total_value += value * fraction
            selected_items.append((value, weight, fraction))  
            break
        
    # Print selected items and fractions
    print("Selected items and their fractions:")
    for value, weight, fraction in selected_items:
        print(f"Item with value {value} and weight {weight}: fraction taken = {fraction:.2f}")

        
    return total_value

# List of items: (value, weight)
items = [
    (10, 2),  
    (5, 3), 
    (15, 5),
    (7, 7),
    (6, 1),
    (18, 4),
    (3, 1), 
]

# Maximum weight capacity of the knapsack
capacity = 15

# Solve the problem
max_value = fractional_knapsack(items, capacity)
print(f"Maximum value that can be carried: {max_value}")
    