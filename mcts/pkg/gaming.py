import pkg.tictactoe as tictactoe
import random
import pkg.agents as agents
def PlayGame(args):
    game_number, verbose, itermax1, itermax2, selection1, selection2 = args
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    assert selection1 is not None
    assert selection2 is not None
    state = tictactoe.TicTacToe()
    while (state.GetMoves() != []):
        if verbose:
            print(str(state))
        if state.LastPlayer() == 1:
            m = agents.Agent(rootstate=state, itermax=itermax1, verbose=False, selection=selection1)
        else:
            m = agents.Agent(rootstate=state, itermax=itermax2, verbose=False, selection=selection1)
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

def PlayRandomGame(args):
    game_number, verbose, itermax1, itermax2, selection1, selection2 = args
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    assert selection1 is not None
    assert selection2 is not None
    state = tictactoe.TicTacToe()
    state.SetLastPlayer(random.choice([1, 2]))
    while (state.GetMoves() != []):
        if verbose:
            print(str(state))
        if state.LastPlayer() == 1:
            m = agents.Agent(rootstate=state, itermax=itermax1, verbose=False, selection=selection1)
        else:
            m = agents.Agent(rootstate=state, itermax=itermax2, verbose=False, selection=selection1)
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