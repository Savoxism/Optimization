import os


def max_heapify(a, i, n):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2

    if left < n and a[left] > a[largest]:
        largest = left
        
    if right < n and a[right] > a[largest]:
        largest = right
    
    if largest != i:
        a[i], a[largest] = a[largest], a[i]
        max_heapify(a, n, largest)

def build_max_heap(a):
    n = len(a)
    for i in range(n // 2 - 1, -1, -1):
        max_heapify(a, n, i)

def heap_sort(a):
    n = len(a)
    build_max_heap(a)
    
    for end in range(n - 1, 0, -1):
        a[0], a[end] = a[end], a[0]
        max_heapify(a, end, 0)
    return a

arr = [7, 2, 9, 4, 1, 5]
heap_sort(arr)
print("Sorted array:", arr)