def fibo(n):
    if n < 2:
        return n
    
    x = 0
    y = 1
    for _ in range(2, n+1):
        z = x + y
        x = y
        y = z
        
    return y

FibArray = [0, 1]
def fibonacci(n):
    if n < 0:
        print("Incorrect input")
    elif n <= len(FibArray):
        return FibArray[n-1]
    else:
        temp_fib = fibonacci(n-1) + fibonacci(n-2)
        FibArray.append(temp_fib)
        return temp_fib
    
print(fibo(12312321))