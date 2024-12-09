import random
import pkg.tictactoe as tictactoe
import numpy as np
from math import sqrt, log
from pkg.node import Node
from pkg.selection import selectionpolicy
from multiprocessing import Pool
from tqdm import tqdm
from pkg.gui import TicTacToeGUI
import pkg.agent as agent
import tkinter as tk
def playGame(verbose=False, agent1=None, agent2=None):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = tictactoe.TicTacToe()
    while (state.GetMoves() != []):
        if verbose:
            print(str(state))
        if state.LastPlayer() == 1:
            m = agent1.play(state)
        else:
            m = agent2.play(state)
        if verbose: print("Best Move: " + str(m) + "\n")

    result = state.GetResult(state.LastPlayer())
    winning = False
    winner = None
    if result == 1:
        winner = state.LastPlayer()
        winning = True
        if verbose:
            print("Player " + str(state.LastPlayer()) + " wins!")
    elif result == -1:
        winner = 3 - state.LastPlayer()
        winning = True
        if verbose:
            print("Player " + str(3 - state.LastPlayer()) + " wins!")
    else:
        if verbose:
            print("Nobody wins!")
    if verbose:
        print(str(state))

    return (winning, winner)

def human_vs_ai(agent1, agent2):
    """ Let a human play TicTacToe against the AI using the GUI. """
    root = tk.Tk()
    game = tictactoe.TicTacToe()
    gui = TicTacToeGUI(root)
    def on_click(i, j):
        if agent1.play(game, gui, i, j):
            return
        if agent2.play(game, gui, i, j):
            return

    gui.on_click = on_click
    root.mainloop()


if __name__ == "__main__":
    agent1 = agent.AIAgent(train="UCT", test="UCT", itermax=100)
    agent1.train(1000)
    agent2 = agent.AIAgent(train="UCT", test="UCT", itermax=10)
    agent2.train(1000)
    num_games = 1000
    results_list = []
    for _ in tqdm(range(num_games), desc="Playing Progress"):
        results_list.append(playGame(agent1=agent1, agent2=agent2))
    pos = 0
    neg = 0
    player1 = 0
    player2 = 0
    for result in results_list:
        if result[0]:
            pos += 1
            if result[1] == 1:
                player1 += 1
            elif result[1]:
                player2 += 1
        else:
            neg += 1
    print("Number of positives: %d / %d" % (pos, num_games))
    print("Number of negatives: %d / %d" % (neg, num_games))
    print("Player1 wins: %2.2f%%" % (float(player1) / pos * 100))
    print("Player2 wins: %2.2f%%" % (float(player2) / pos * 100))
    # main()