import sys 

def read_input():
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
        constraints.append((x_i, x_j, d))  

    return n, domains, constraints

# Enforces domain consistency for the CSP using LEQ constraints.
def enforce_domain_consistency(n, domains, constraints):
    queue = list(constraints)  #

    while queue:
        i, j, d = queue.pop(0)  
        i -= 1  # Convert to 0-based indexing internally
        j -= 1  # Convert to 0-based indexing internally
        new_domain_i = set()

        for val_i in domains[i]:
            valid = False
            for val_j in domains[j]:
                if val_i <= val_j + d:
                    valid = True
                    break
            if valid:
                new_domain_i.add(val_i)

        if new_domain_i != domains[i]:
            domains[i] = new_domain_i
            if not domains[i]:
                return "FAIL" 

            # Re-enqueue constraints that depend on i
            for x_i, x_j, d_k in constraints:
                if x_i == i + 1: 
                    queue.append((x_i, x_j, d_k))

    return domains

        
def main():
    n, domains, constraints = read_input()
    result = enforce_domain_consistency(n, domains, constraints)

    if result == "FAIL":
        print("FAIL")
    else:
        for domain in result:
            print(len(domain), " ".join(map(str, sorted(domain))) + " ")

if __name__ == "__main__":
    main()