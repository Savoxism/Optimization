import math
import time

EMPTY, PLAYER, AI = ' ', 'X', 'O'

def create_board():
    return [[EMPTY for _ in range(3)] for _ in range(3)]

def print_board(board):
    print("\n".join([" | ".join(row) + "\n" + "-" * 9 for row in board]))

def is_game_over(board):
    return check_winner(board, PLAYER) or check_winner(board, AI) or all(cell != EMPTY for row in board for cell in row)

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
        
    return all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3))

def minimax(board, depth, alpha, beta, is_maximizing):
    if check_winner(board, AI):
        return 10
    if check_winner(board, PLAYER):
        return -10
    if is_game_over(board):
        return 0

    if is_maximizing: # Maximizing player: AI
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
    best_eval, best_move = -math.inf, None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = AI
                eval = minimax(board, 0, -math.inf, math.inf, False)
                board[i][j] = EMPTY
                if eval > best_eval:
                    best_eval, best_move = eval, (i, j)
    return best_move

def check_game_state(board):
    if check_winner(board, PLAYER):
        print("You win!")
        return True
    if check_winner(board, AI):
        print("AI wins!")
        return True
    if is_game_over(board):
        print("It's a tie!")
        return True
    return False

def play_game():
    board = create_board()
    print("Welcome to Tic-Tac-Toe! You are 'X', and the AI is 'O'.")
    print_board(board)

    while True:
        while True:
            try:
                player_move = input("Enter your move (row col, e.g., 0 0 for top-left): ")
                row, col = map(int, player_move.split())
                if row not in range(3) or col not in range(3):
                    print("Invalid move! Row and column must be 0, 1, or 2.")
                    continue
                if board[row][col] != EMPTY:
                    print("Invalid move! Cell is already occupied.")
                    continue
                break
            except ValueError:
                print("Invalid input! Please enter two integers separated by a space.")

        board[row][col] = PLAYER
        print_board(board)

        if check_game_state(board):
            break

        print("AI is thinking...")
        time.sleep(1)
        ai_move = find_best_move(board)
        board[ai_move[0]][ai_move[1]] = AI
        print_board(board)

        if check_game_state(board):
            break

play_game()