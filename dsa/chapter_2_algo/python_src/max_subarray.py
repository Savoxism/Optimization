
array = [-2, 11, -4, 13, -5, 2]

max_so_far = array[0]
max_sum = array[0]

for i in range(1, len(array)):
    max_sum= max(array[i], max_sum + array[i])
    max_so_far = max(max_so_far, max_sum)

print(max_so_far)  # 20