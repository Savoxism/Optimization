def partition(arr, low, high):
    pivot = arr[high]
    
    i = low - 1
    
    for j in range(low, high):
        if arr[j] < pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
        else:
            continue
        
    # Move the pivot to its correct position 
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    
    return i + 1

def quick_sort(arr, low, high):
    if low < high:
        partition_index = partition(arr, low, high)\
            
        # Perform quick sort on the left and right sub-arrays
        quick_sort(arr, low, partition_index - 1)
        
        quick_sort(arr, partition_index + 1, high)
        
    return arr

arr = [64, 25, 12, 22, 11]
print(quick_sort(arr, 0, len(arr) - 1))  # Output: [11, 12, 22, 25, 64]