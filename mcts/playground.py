import pkg.tictactoe as tictactoe
import random
import pkg.agents as agents
from pkg.gui import TicTacToeGUI
import tkinter as tk
from multiprocessing import Pool
import pkg.gaming as gaming
from tqdm import tqdm
def human_vs_ai(itermax,selection):
    """ Let a human play TicTacToe against the AI using the GUI. """
    number_of_games = 1000
    agent = agents.Agent(itermax=itermax, verbose=False, selection=selection)
    agent_ = agents.Agent(itermax=itermax, verbose=False, selection=selection)
    for _ in tqdm(range(number_of_games), desc="Playing games"):
        state = tictactoe.TicTacToe()
        state.SetLastPlayer(random.choice([1, 2]))
        while (state.GetMoves() != []):
            if state.LastPlayer() == 1:
                m = agent.predict(state)
            else:
                m = agent_.predict(state)
            state.DoMove(m)

            if state.HasWinning(): break
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
            m = agent.predict(game)
            print("m",m)
            game.DoMove(m)
            gui.game = game.Clone()
            gui.update_board()
            if game.HasWinning():
                gui.show_winner()
                return
    gui.on_click = on_click
    root.mainloop()
def huamn_vs_human():
    root = tk.Tk()
    gui = TicTacToeGUI(root)
    root.mainloop()

if __name__ == "__main__":
    human_vs_ai(150, "UCT")
    # huamn_vs_human()
