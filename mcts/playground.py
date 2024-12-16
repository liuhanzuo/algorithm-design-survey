import pkg.tictactoe as tictactoe
import random
import pkg.agents as agents
from pkg.gui import TicTacToeGUI
import tkinter as tk
def human_vs_ai(itermax,selection):
    """ Let a human play TicTacToe against the AI using the GUI. """
    root = tk.Tk()
    game = tictactoe.TicTacToe()
    gui = TicTacToeGUI(root)
    def on_click(x, y):
        if game.GetMoves() == []:
            return
        if game.LastPlayer() == 1:
            move = x * 3 + y
            game.DoMove(move)
            gui.game = game.Clone()
            gui.update_board()
            if game.HasWinning():
                gui.show_winner()
                return
        else:
            m = agents.Agent(rootstate=game, itermax=itermax, verbose=False, selection=selection)
            print("m",m)
            game.DoMove(m)
            gui.game = game.Clone()
            gui.update_board()
            if game.HasWinning():
                gui.show_winner()
                return
    gui.on_click = on_click
    root.mainloop()
if __name__ == "__main__":
    human_vs_ai(40, "reward")
