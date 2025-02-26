
def counting_sort(arr, exp):
    n = len(arr)
    
    output = [0] * n
    
    count = [0] * 10
    
    for i in range(0, n):
        index = arr[i] // exp
        count[index % 10] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]    
        
    # Build the output array
    i = n - 1
    while i >= 0:
        index = arr[i] // exp
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1

    i = 0
    for i in range(0, len(arr)):
        arr[i] = output[i]
        
def radix_sort(arr):
    max1 = max(arr)
    
    exp = 1
    
    while max1 // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
        
    return arr
        
        
arr = [170, 45, 75, 90, 802, 24, 2, 66]
print(radix_sort(arr))    
    