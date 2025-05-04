import time
import sys

# Increase recursion limit
sys.setrecursionlimit(3000)  # Set a

def fibo_tabu(n):
    
    if n <= 1:
        return n
    
    fib = [-1] * (n + 1)
    fib[0] = 0  
    fib[1] = 1
    
    for i in range(2, n + 1):
        fib[i] = fib[i - 1] + fib[i - 2]
        
    return fib[n]

def fibo_top_down(n, memo=None):
    # Initialize the memoization table
    if memo is None:
        memo = {}
        
    # Base case
    if n <= 1:
        return n
    
    if n in memo:
        return memo[n]
    
    
    memo[n] = fibo_top_down(n - 1, memo) + fibo_top_down(n - 2, memo)
    return memo[n]

def compare_execution_time(n):
    # Measure execution time for fibo_tabu
    start_time = time.time()
    fib_tabu_result = fibo_tabu(n)
    end_time = time.time()
    tabu_time = end_time - start_time
    print(f"fibo_tabu({n}) = {fib_tabu_result}, Execution Time: {tabu_time:.6f} seconds")

    # Measure execution time for fibo_top_down
    start_time = time.time()
    fib_top_down_result = fibo_top_down(n)
    end_time = time.time()
    top_down_time = end_time - start_time
    print(f"fibo_top_down({n}) = {fib_top_down_result}, Execution Time: {top_down_time:.6f} seconds")

    # Compare times
    if tabu_time < top_down_time:
        print(f"Tabulation is faster by {top_down_time - tabu_time:.6f} seconds")
    else:
        print(f"Top-down is faster by {tabu_time - top_down_time:.6f} seconds")


compare_execution_time(2220)