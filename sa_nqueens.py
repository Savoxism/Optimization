import random 
import math 

def generate_initial_state(n):
    state = list(range(n))
    random.shuffle(state)
    check1 = [state[j] - j for j in range(n)]
    check2 = [state[j] + j for j in range(n)]
    
    for i in range(n):
        h_row[i] = state.count(i)
    
    for i in range(-n + 1, n): 
        h_diagonal1[i] = check1.count(i)
    
    for k in range(2 * n - 1):
        h_diagonal2[k] = check2.count(k)

    return state

def calculate_initial_violations(state):
    v = 0
    for i in range(len(state)):
        for j in range(i + 1, len(state)):
            if state[i] == state[j]:
                v += 1
            if state[i] + i == state[j] + j:
                v += 1
            if state[i] - i == state[j] - j:
                v += 1
    return v

def violations_upgrade(queen, r, old_vio):
    new_vio = h_row[r] + h_diagonal1[r - queen] + h_diagonal2[r + queen] + old_vio - h_row[state[queen]] - h_diagonal1[state[queen] - queen] - h_diagonal2[state[queen] + queen] + 3
    
    return new_vio

def select_most_violating_queen():
    def violations_per_queen(queen):
          return h_row[state[queen]] + h_diagonal1[state[queen] - queen] + h_diagonal2[state[queen] + queen] - 3
      
    max_violations = 0
    candidates = []
    
    for i in range(n):
        violations = violations_per_queen(i)
        if violations > max_violations:
            max_violations = violations
            candidates = [i]
        elif violations == max_violations:
            candidates.append(i)

    return random.choice(candidates)

# Find the best row to reduce conflicts for a given queen
def select_most_promising_row(queen, violations):
    def get_delta(queen, r, violations):
        return violations_upgrade(queen, r, violations) - violations

    min_delta = float('inf')
    candidates = []

    for r in range(n):
        delta = get_delta(queen, r, violations)
        if delta < min_delta:
            min_delta = delta
            candidates = [r]
        elif delta == min_delta:
            candidates.append(r)

    return random.choice(candidates)


# Perform one iteration of the Metropolis algorithm
def s_metropolis():
    global temperature, violations

    # Randomly decide between local and random exploration
    if random.random() > 0.3:
        queen = select_most_violating_queen()
        row = select_most_promising_row(queen, violations)
    else:
        queen = random.randint(0, n - 1)
        row = random.choice([r for r in range(n) if r != state[queen]])

    delta_violations = violations_upgrade(queen, row, violations)

    if delta_violations == 0:
        # Update the conflict trackers
        h_row[state[queen]] -= 1
        h_diagonal1[state[queen] - queen] -= 1
        h_diagonal2[state[queen] + queen] -= 1
        h_row[row] += 1
        h_diagonal1[row - queen] += 1
        h_diagonal2[row + queen] += 1

        state[queen] = row
        violations = 0
        return True

    elif delta_violations <= violations:
        # Update state with better or equal move
        h_row[state[queen]] -= 1
        h_diagonal1[state[queen] - queen] -= 1
        h_diagonal2[state[queen] + queen] -= 1
        h_row[row] += 1
        h_diagonal1[row - queen] += 1
        h_diagonal2[row + queen] += 1

        state[queen] = row
        violations = delta_violations
        return False

    else:
        # Accept worse move probabilistically
        if random.random() < math.exp((violations - delta_violations) / temperature):
            h_row[state[queen]] -= 1
            h_diagonal1[state[queen] - queen] -= 1
            h_diagonal2[state[queen] + queen] -= 1
            h_row[row] += 1
            h_diagonal1[row - queen] += 1
            h_diagonal2[row + queen] += 1

            state[queen] = row
            violations = delta_violations

        return False

# Simulated annealing algorithm
def simulate_annealing():
    global best_state, best_vio, temperature

    for _ in range(MAX_ITER):
        if s_metropolis():
            best_state[:] = state[:]
            best_vio = violations
            break

        if violations < best_vio:
            best_vio = violations
            best_state[:] = state[:]

        temperature *= cooling_rate
        if temperature < 0.001:
            break
        
# Main execution
n = int(input())

# Initialize conflict trackers
h_row = [0] * n
h_diagonal1 = [0] * (2 * n - 1)
h_diagonal2 = [0] * (2 * n - 1)

MAX_ITER = 100000
state = generate_initial_state(n)
best_state = state[:]
violations = calculate_initial_violations(state)
best_vio = violations

# Simulated annealing parameters
temperature = 10000
cooling_rate = 0.99

simulate_annealing()

# Output results
if best_vio == 0:
    print(n)
    print(" ".join(str(x + 1) for x in best_state))
else:
    print("No solution found")
