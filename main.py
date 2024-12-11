tableau = [
        [2.0, 1.0, 1, 0, 0, 7.0], #0th row
        [1.0, 2.0, 0, 1, 0, 8.0], #1st row
        [1.0, -1.0, 0, 0, 1, 2.0], #2nd row
        [-3.0, -2.0, 0, 0, 0.0, 0.0]  # Objective row
    ]

entering = tableau[-1][:-1].index(min(tableau[-1][:-1]))    

# print(entering) # 0

ratios = []
for row in tableau[:-1]:
    if row[entering] > 0:
        ratios.append(row[-1] / row[entering])
    else:
        ratios.append(float('inf'))
leaving = ratios.index(min(ratios))
# print(leaving) # 0
pivot = tableau[leaving][entering]
# print(pivot) # 2.0

tableau[leaving] = [x / pivot for x in tableau[leaving]]

# print(tableau[leaving])

for i, row in enumerate(tableau):
    if i != leaving:
        factor = row[entering]
        tableau[i] = [row[j] - factor * tableau[leaving][j] for j in range(len(row))]
        
        
print(tableau)