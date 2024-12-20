def calculate_all_different(variables):
    violations = 0
    for i in range(len(variables)):
        for j in range(i + 1, len(variables)):
            if variables[i] == variables[j]:
                violations += 1
    return violations


variables = [1, 1, 3, 3, 4]

print(calculate_all_different(variables)) # Expected output: 1