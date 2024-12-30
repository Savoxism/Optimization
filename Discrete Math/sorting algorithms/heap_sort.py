


def max_heap(arr, n, i):
    
    largest = i
    
    left = 2 * i + 1 # Left child index
    
    right = 2 * i + 2 # Right child index
    
    # Check if left child exists and is greater than the root
    if left < n and arr[left] > arr[largest]:
        largest = left
        
    if right < n and arr[right] > arr[largest]:
        largest = right
        
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        
        max_heap(arr, n, largest)
        

def heap_sort(arr):
    
    n = len(arr)
    
    for i in range(n // 2 - 1, -1, -1):
        max_heap(arr, n, i)
        
    # Step 2: Extract elements one by one
    for i in range(n - 1, 0, -1):
        # Swap the root (largest) with the last element
        arr[0], arr[i] = arr[i], arr[0]

        # Reduce the size of the heap and heapify the root
        max_heap(arr, i, 0)

    return arr


arr = [64, 25, 12, 22, 11]
print(heap_sort(arr)) 