import tkinter as tk
from tkinter import messagebox, simpledialog
import random

# Create main window
root = tk.Tk()
root.title("Tic-Tac-Toe")
root.configure(bg="#121212")
root.resizable(False, False)

# Game state variables
current_player = "X"
board = [""] * 9
buttons = []
scores = {"X": 0, "O": 0}
player_names = {"X": "Player X", "O": "Player O"}
vs_computer = False
wins = [(0,1,2), (3,4,5), (6,7,8), (0,3,6), (1,4,7), (2,5,8), (0,4,8), (2,4,6)]

# Score display
score_lbl = tk.Label(root, text="", font=("Arial", 14), bg="#121212", fg="#ffffff")
score_lbl.grid(row=3, column=0, columnspan=3, pady=(10, 0))

def update_score_label():
    score_lbl.config(text=f"{player_names['X']} (X): {scores['X']}  |  {player_names['O']} (O): {scores['O']}")

def check_winner():
    for a, b, c in wins:
        if board[a] == board[b] == board[c] != "":
            for i in (a, b, c):
                buttons[i].config(bg="#2ecc71")
            scores[board[a]] += 1
            update_score_label()
            messagebox.showinfo("Game Over", f"{player_names[board[a]]} wins!")
            disable_all()
            return True
    if "" not in board:
        messagebox.showinfo("Game Over", "It's a draw!")
        return True
    return False

def on_click(index):
    global current_player
    if board[index] == "":
        board[index] = current_player
        buttons[index].config(text=current_player, fg="#00ace6" if current_player == "X" else "#ff4d4d")
        if not check_winner():
            current_player = "O" if current_player == "X" else "X"
            if vs_computer and current_player == "O":
                root.after(500, ai_move)

def disable_all():
    for btn in buttons:
        btn.config(state="disabled")

def reset_board():
    global current_player, board
    current_player = "X"
    board = [""] * 9
    for btn in buttons:
        btn.config(text="", state="normal", bg="#1e1e1e")

def reset_game():
    scores["X"] = 0
    scores["O"] = 0
    update_score_label()
    reset_board()

def ai_move():
    empty = [i for i in range(9) if board[i] == ""]
    if empty:
        index = random.choice(empty)
        on_click(index)

def ask_players():
    global vs_computer
    choice = messagebox.askyesno("Game Mode", "Play vs Computer?\nYes = vs Computer\nNo = 2 Players")
    vs_computer = choice
    player_names["X"] = simpledialog.askstring("Name", "Enter Player X's name:") or "Player X"
    if vs_computer:
        player_names["O"] = "Computer"
    else:
        player_names["O"] = simpledialog.askstring("Name", "Enter Player O's name:") or "Player O"
    update_score_label()

# Create game buttons
for i in range(9):
    btn = tk.Button(root, text="", font=("Arial", 32), width=4, height=2,
                    bg="#1e1e1e", fg="#ffffff", activebackground="#333333",
                    command=lambda i=i: on_click(i))
    btn.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(btn)

# Reset/Restart button frame
btn_frame = tk.Frame(root, bg="#121212")
btn_frame.grid(row=4, column=0, columnspan=3, pady=10)

tk.Button(btn_frame, text="Reset Board", font=("Arial", 12), bg="#e67e22", fg="white", command=reset_board).pack(side="left", padx=10)
tk.Button(btn_frame, text="Reset Score", font=("Arial", 12), bg="#9b59b6", fg="white", command=reset_game).pack(side="left", padx=10)

# Delay player name input to avoid UI freeze
root.after(100, ask_players)
root.mainloop()