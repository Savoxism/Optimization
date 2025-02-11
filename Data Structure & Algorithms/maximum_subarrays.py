def max_subarray_brute_force(arr):
    max_sum = float('-inf')  # Initialize with negative infinity
    largest_subarray = []

    for i in range(len(arr)):
        current_sum = 0
        current_subarray = []

        for j in range(i, len(arr)):
            current_sum += arr[j]
            current_subarray.append(arr[j])

            if current_sum > max_sum:
                max_sum = current_sum
                largest_subarray = current_subarray[:]

    return max_sum, largest_subarray

##### DYNAMIC PROGRAMMING #####
def max_subarray_sum(nums):
    smax = nums[0]  # Overall maximum subarray sum
    ei = nums[0]     # Max subarray sum ending at index i

    for i in range(1, len(nums)):
        ei = max(nums[i], ei + nums[i])  
        smax = max(smax, ei)  

    return smax


array = [-2, 11, -4, 13, -5, 2]
print(max_subarray_brute_force(array))  # (20, [11, -4, 13])
print(max_subarray_sum(array))  # 20

