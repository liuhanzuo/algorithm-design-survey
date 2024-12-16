import tkinter as tk
from pkg.tictactoe import TicTacToe

class TicTacToeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.game = TicTacToe()
        self.buttons = []
        self.create_board()

    def create_board(self):
        for i in range(3):
            row = []
            for j in range(3):
                button = tk.Button(self.root, text="", width=10, height=3, command=lambda i=i, j=j: self.on_click(i, j))
                button.grid(row=i, column=j)
                row.append(button)
            self.buttons.append(row)

    def on_click(self, i, j):
        index = i * 3 + j
        if self.game.board[index] == 0:
            self.game.DoMove(index)
            self.update_board()
            if self.game.HasWinning():
                self.show_winner()
            elif not self.game.HasRemainingMove():
                self.show_draw()
    def update_click(self, index):
        self.game.board[index] = self.game.LastPlayer()
        self.game.UpdatePlayer()
        self.update_board()
    def update_board(self):
        for i in range(3):
            for j in range(3):
                index = i * 3 + j
                self.buttons[i][j].config(text=".XO"[self.game.board[index]])

    def show_winner(self):
        winner = "Player " + str(self.game.LastPlayer()) + " wins!"
        self.show_message(winner)

    def show_draw(self):
        self.show_message("It's a draw!")

    def show_message(self, message):
        popup = tk.Toplevel()
        popup.title("Game Over")
        label = tk.Label(popup, text=message)
        label.pack(side="top", fill="x", pady=10)
        ok_button = tk.Button(popup, text="OK", command=self.root.quit)
        ok_button.pack()

if __name__ == "__main__":
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()
