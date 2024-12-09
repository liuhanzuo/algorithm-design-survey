import random
import pkg.tictactoe as tictactoe
import numpy as np
from math import sqrt, log
from pkg.node import Node
from pkg.selection import selectionpolicy
from multiprocessing import Pool
from tqdm import tqdm
from pkg.gui import TicTacToeGUI
import tkinter as tk


def policyagent(rootstate, itermax, verbose=False, selection="UCT"):
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

    rootnode = Node(state=rootstate)
    sp = selectionpolicy(selection)
    for i in range(itermax):
        node = rootnode
        state = rootstate.Clone()

        # Select
        # Initially a node has not child
        while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
            node = sp.select(node)
            state.DoMove(node.move)

        # Expand
        # if we can expand (i.e. state/node is non-terminal)
        # select a move randomly, create a child and let him keep tack of the move
        # that created it. Then return the child (node) and continue from it
        if node.untriedMoves != []:
            m = random.choice(node.untriedMoves)
            state.DoMove(m)
            node = node.AddChild(m, state)  # add child and descend tree

        # Rollout - this can often be made orders of magnitude quicker using a state.GetRandomMove() function
        while state.GetMoves() != [] and not state.HasWinning():  # while state is non-terminal
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while node != None:  # backpropagate from the expanded node and work back to the root node
            # state is terminal. Update node with result from POV of node.playerJustMoved
            node.Update(state.GetResult(node.playerJustMoved))
            node = node.parentNode

    # Output some information about the tree - can be omitted
    # if (verbose):
    #     print(rootnode.TreeToString(0))
    #     print(rootnode.ChildrenToString())

    # return the move that was most visited
    return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move


def PlayGame(game_number, verbose=False):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = tictactoe.TicTacToe()
    while (state.GetMoves() != []):
        if verbose:
            print(str(state))
        if state.LastPlayer() == 1:
            # play with values for itermax and verbose = True
            # m = np.random.choice(state.GetMoves())
            m = policyagent(rootstate=state, itermax=80, verbose=False, selection="UCT")
        else:
            m = policyagent(rootstate=state, itermax=80, verbose=False, selection="reward")
        if verbose: print("Best Move: " + str(m) + "\n")
        state.DoMove(m)

        if state.HasWinning(): break

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

def playGame(game_number, verbose=False, iteration=80):
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    state = tictactoe.TicTacToe()
    while (state.GetMoves() != []):
        if verbose:
            print(str(state))
        if state.LastPlayer() == 1:
            # play with values for itermax and verbose = True
            # m = np.random.choice(state.GetMoves())
            m = policyagent(rootstate=state, itermax=iteration, verbose=False, selection="UCT")
        else:
            m = policyagent(rootstate=state, itermax=iteration, verbose=False, selection="reward")
        if verbose: print("Best Move: " + str(m) + "\n")
        state.DoMove(m)

        if state.HasWinning(): break

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

def human_vs_ai(itermax=10, selection="UCT"):
    """ Let a human play TicTacToe against the AI using the GUI. """
    root = tk.Tk()
    game = tictactoe.TicTacToe()
    gui = TicTacToeGUI(root)
    
    def on_click(i, j):
        index = i * 3 + j
        if game.board[index] == 0:
            game.DoMove(index)
            gui.update_click(index)
            print(index)
            if game.HasWinning():
                gui.show_winner()
                return
            elif not game.HasRemainingMove():
                gui.show_draw()
                return
            ai_move = policyagent(rootstate=game, itermax=itermax, selection=selection)
            game.DoMove(ai_move)
            print(ai_move)
            gui.update_click(ai_move)
            if game.HasWinning():
                gui.show_winner()
            elif not game.HasRemainingMove():
                gui.show_draw()

    gui.on_click = on_click
    root.mainloop()

def main():
    """ Play a several game to the end using UCT for both players.
    """

    number_of_games = 1000

    results_list = []

    # processing
    pool = Pool(processes=8)
    for result in tqdm(pool.imap_unordered(PlayGame, range(number_of_games)),
                       total=number_of_games):
      results_list.append(result)
    # compiling results
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

    print("Number of positives: %d / %d" % (pos, number_of_games))
    print("Number of negatives: %d / %d" % (neg, number_of_games))
    print("Player1 wins: %2.2f%%" % (float(player1)/pos*100))
    print("Player2 wins: %2.2f%%" % (float(player2)/pos*100))


if __name__ == "__main__":
    human_vs_ai()
    # main()