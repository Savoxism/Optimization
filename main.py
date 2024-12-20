def read_input():
    """Reads the input and returns the variables, domains, and constraints."""
    import sys
    input = sys.stdin.read
    lines = input().strip().split("\n")

    # Number of variables
    n = int(lines[0])

    # Read domains of variables
    domains = []
    for i in range(1, n + 1):
        line = list(map(int, lines[i].split()))
        k = line[0]
        domains.append(set(line[1:k + 1]))

    # Number of constraints
    m = int(lines[n + 1])

    # Read constraints
    constraints = []
    for i in range(n + 2, n + 2 + m):
        x_i, x_j, d = map(int, lines[i].split())
        constraints.append((x_i - 1, x_j - 1, d))  # Convert to 0-based indexing

    return n, domains, constraints

def enforce_domain_consistency(n, domains, constraints):
    """Enforces domain consistency for the CSP using LEQ constraints."""
    queue = list(constraints)  # Use a list instead of deque

    while queue:
        i, j, d = queue.pop(0)  # Pop the first element
        new_domain_i = set()

        for val_i in domains[i]:
            # Check if val_i satisfies the constraint with any value in domain[j]
            if any(val_i <= val_j + d for val_j in domains[j]):
                new_domain_i.add(val_i)

        if new_domain_i != domains[i]:
            domains[i] = new_domain_i
            if not domains[i]:
                return "FAIL"  # If a domain becomes empty, return FAIL

            # Re-enqueue all constraints where i is involved
            for x_i, x_j, d_k in constraints:
                if x_i == i or x_j == i:
                    queue.append((x_i, x_j, d_k))

    return domains

def main():
    """Main function to execute the program."""
    n, domains, constraints = read_input()
    result = enforce_domain_consistency(n, domains, constraints)

    if result == "FAIL":
        print("FAIL")
    else:
        for idx, domain in enumerate(result):
            print(len(domain), " ".join(map(str, sorted(domain))) + " ")

if __name__ == "__main__":
    main()
