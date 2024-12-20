# N-queens using backtracking
n = 4
board = [-1] * n # board[i] = j means there is a queen at (i, j)
results = []

def is_safe(row, col):
    for i in range(row):
        if board[i] == col or abs(i - row) == abs(board[i] - col):
            return False
    return True

def solve_n_queens(row, n, board, results):
    # base case
    if row == n:
        results.append(board[:])
        return 
    
    for col in range(n):
        if is_safe(row, col):
            board[row] = col
            solve_n_queens(row + 1, n, board, results)
            board[row] = -1
            
solve_n_queens(0, n, board, results)

print(results)