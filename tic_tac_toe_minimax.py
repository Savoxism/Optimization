import math

EMPTY = ' '
PLAYER = 'X'
AI = 'O'

def create_board():
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    return board 

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)
        
def is_terminated(board):
    return all(cell != EMPTY for row in board for cell in row)

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # Rows
            return True
        if all(board[j][i] == player for j in range(3)):  # Columns
            return True
    if all(board[i][i] == player for i in range(3)):  # Main diagonal
        return True
    if all(board[i][2 - i] == player for i in range(3)):  # Anti-diagonal
        return True
    return False

def evaluate(board):
    max_open = count_open_lines(board, AI)
    min_open = count_open_lines(board, PLAYER)
    return max_open - min_open

def count_open_lines(board, player):
    count = 0
    for i in range(3):
        if all(board[i][j] == player or board[i][j] == EMPTY for j in range(3)):  # Rows
            count += 1
        if all(board[j][i] == player or board[j][i] == EMPTY for j in range(3)):  # Columns
            count += 1
    # Check diagonals
    if all(board[i][i] == player or board[i][i] == EMPTY for i in range(3)):  # Main diagonal
        count += 1
    if all(board[i][2 - i] == player or board[i][2 - i] == EMPTY for i in range(3)):  # Anti-diagonal
        count += 1
    return count

def minimax(board, depth, alpha, beta, is_maximizing):
    
    if check_winner(board, AI):
        return 10 - depth
    
    if check_winner(board, PLAYER):
        return -10 + depth
    
    if is_terminated(board):
        return 0
    
    # This is the AI turn
    if is_maximizing:
        max_eval = -math.inf
        
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = AI
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    
                    if beta <= alpha:
                        break
                    
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval
    
def find_best_move(board):
    best_eval = -math.inf
    best_move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                eval = minimax(board, 0, -math.inf, math.inf, False)
                board[i][j] = EMPTY
                if eval > best_eval:
                    best_eval = eval
                    best_move = (i, j)
    return best_move



# Main game loop
def play_game():
    board = create_board()
    print("Welcome to Tic-Tac-Toe! You are 'X', and the AI is 'O'.")
    print_board(board)

    while True:
        player_move = input("Enter your move (row col, e.g., 0 0 for top-left): ")
        row, col = map(int, player_move.split())
        if board[row][col] != EMPTY:
            print("Invalid move! Try again.")
            continue
        board[row][col] = PLAYER
        print_board(board)

        # Check if player wins
        if check_winner(board, PLAYER):
            print("You win!")
            break
        if is_terminated(board):
            print("It's a tie!")
            break

        # AI's turn
        print("AI is thinking...")
        ai_move = find_best_move(board)
        board[ai_move[0]][ai_move[1]] = AI
        print_board(board)

        # Check if AI wins
        if check_winner(board, AI):
            print("AI wins!")
            break
        if is_terminated(board):
            print("It's a tie!")
            break

# Run the game
play_game()