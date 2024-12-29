

def merge_sort(arr):
    n = len(arr)
    
    if n > 1:
        mid = n // 2
        left = arr[:mid]
        right = arr[mid:]
        
        merge_sort(left)
        merge_sort(right)
        
        
        i = 0 # index of the left half
        j = 0 # index of the right half
        k = 0 # index of the sorted array
        
        while i < len(left) and j < len(right):
            if left[i] < right[j]: # if the element in the left half is smaller
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
                
            k += 1
            
        # Copy the remaining elements of left half
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
            
        # Copy the remaining elements of right half
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1
            
    return arr

arr = [64, 25, 12, 22, 11]
print(merge_sort(arr))  # Output: [11, 12, 22, 25, 64]
