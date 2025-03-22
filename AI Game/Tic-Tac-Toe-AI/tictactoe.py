import tkinter as tk
from tkinter import messagebox

# ---------------------- Core Game Logic ----------------------

def check_winner(board, player):
    """Check if the specified player has won the game."""
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True
    return False

def highlight_winner(board, player):
    """Highlight the winning combination on the board."""
    for i in range(3):
        if all(board[i][j] == player for j in range(3)):  # Horizontal win
            for j in range(3):
                buttons[i][j].config(bg='lightgreen')
        if all(board[j][i] == player for j in range(3)):  # Vertical win
            for j in range(3):
                buttons[j][i].config(bg='lightgreen')
    if all(board[i][i] == player for i in range(3)):      # Diagonal win (Top-left to bottom-right)
        for i in range(3):
            buttons[i][i].config(bg='lightgreen')
    if all(board[i][2 - i] == player for i in range(3)):  # Diagonal win (Top-right to bottom-left)
        for i in range(3):
            buttons[i][2 - i].config(bg='lightgreen')

def is_board_full(board):
    """Check if the board is completely filled (draw condition)."""
    return all(all(cell != ' ' for cell in row) for row in board)

def minimax(board, depth, is_maximizing, alpha, beta):
    """Minimax algorithm with Alpha-Beta Pruning for efficient AI decision-making."""
    if check_winner(board, 'X'):
        return -1
    if check_winner(board, 'O'):
        return 1
    if is_board_full(board):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ' '
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break  # Prune
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == ' ':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ' '
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break  # Prune
        return min_eval

def best_move(board):
    """Determine the best move for the AI using Minimax with Alpha-Beta Pruning."""
    best_val = float('-inf')
    best_move = None

    for i in range(3):
        for j in range(3):
            if board[i][j] == ' ':
                board[i][j] = 'O'
                move_val = minimax(board, 0, False, float('-inf'), float('inf'))
                board[i][j] = ' '
                if move_val > best_val:
                    best_val = move_val
                    best_move = (i, j)

    return best_move

# ---------------------- Game Flow Logic ----------------------

def make_move(row, col):
    """Player's move logic and win/draw conditions."""
    if board[row][col] != ' ':
        return  # Prevents invalid moves without popup error

    board[row][col] = 'X'
    buttons[row][col].config(text='X', state=tk.DISABLED)

    if check_winner(board, 'X'):
        highlight_winner(board, 'X')
        messagebox.showinfo("Tic-Tac-Toe", "You win!")
        reset_game()
        return

    if is_board_full(board):
        messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
        reset_game()
        return

    ai_move()

def ai_move():
    """AI's turn to make a move."""
    row, col = best_move(board)
    board[row][col] = 'O'
    buttons[row][col].config(text='O', state=tk.DISABLED)

    if check_winner(board, 'O'):
        highlight_winner(board, 'O')
        messagebox.showinfo("Tic-Tac-Toe", "AI wins!")
        reset_game()
        return

    if is_board_full(board):
        messagebox.showinfo("Tic-Tac-Toe", "It's a draw!")
        reset_game()

def reset_game():
    """Reset the game board and UI for a fresh start."""
    global board
    board = [[' ' for _ in range(3)] for _ in range(3)]
    for row in buttons:
        for button in row:
            button.config(text=' ', state=tk.NORMAL, bg='SystemButtonFace')

# ---------------------- Tkinter UI Setup ----------------------

root = tk.Tk()
root.title("Tic-Tac-Toe")

board = [[' ' for _ in range(3)] for _ in range(3)]
buttons = []

# Create Game Board
for i in range(3):
    row_buttons = []
    for j in range(3):
        button = tk.Button(root, text=' ', font=('normal', 30), width=5, height=2, 
                           command=lambda row=i, col=j: make_move(row, col))
        button.grid(row=i, column=j)
        row_buttons.append(button)
    buttons.append(row_buttons)

# Reset Button for Convenience
reset_button = tk.Button(root, text='Reset', font=('normal', 20), command=reset_game)
reset_button.grid(row=3, column=0, columnspan=3, sticky="nsew")

root.mainloop()
