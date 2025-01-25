def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        
        # Last i elements are already in place
        for j in range(0, n - 1 - i):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                
    
    return arr

arr = [64, 25, 12, 22, 11]
print(bubble_sort(arr))  # Output: [11, 12, 22, 25, 64]