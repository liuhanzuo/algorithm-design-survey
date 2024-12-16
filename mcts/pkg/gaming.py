import pkg.tictactoe as tictactoe
import random
import pkg.agents as agents
from tqdm import tqdm
def PlayGame(args):
    train_game_number, test_game_number, verbose, itermax1, itermax2, selection1, selection2 = args
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    assert selection1 is not None
    assert selection2 is not None
    state = tictactoe.TicTacToe()
    agent1 = agents.Agent(itermax=itermax1, verbose=False, selection=selection1)
    agent2 = agents.Agent(itermax=itermax2, verbose=False, selection=selection2)
    for _ in tqdm(range(train_game_number), desc="Playing games"):
        while (state.GetMoves() != []):
            if verbose:
                print(str(state))
            if state.LastPlayer() == 1:
                m = agent1.predict(state)
            else:
                m = agent2.predict(state)
            if verbose: print("Best Move: " + str(m) + "\n")
            state.DoMove(m)

            if state.HasWinning(): break
    win1 = 0
    win2 = 0 
    draw = 0
    for _ in tqdm(range(test_game_number), desc="Playing games"):
        while (state.GetMoves() != []):
            if verbose:
                print(str(state))
            if state.LastPlayer() == 1:
                m = agent1.predict(state)
            else:
                m = agent2.predict(state)
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
        if not winning:
            draw += 1
        elif winner == 1:
            win1 += 1
        else:
            win2 += 1
    return (win1, win2, draw)

def PlayRandomGame(args):
    train_game_number, test_game_number, verbose, itermax1, itermax2, selection1, selection2 = args
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    assert selection1 is not None
    assert selection2 is not None
    state = tictactoe.TicTacToe()
    state.SetLastPlayer(random.choice([1, 2]))
    agent1 = agents.Agent(itermax=itermax1, verbose=False, selection=selection1)
    agent2 = agents.Agent(itermax=itermax2, verbose=False, selection=selection2)
    for _ in tqdm(range(train_game_number), desc="Playing games"):
        while (state.GetMoves() != []):
            if verbose:
                print(str(state))
            if state.LastPlayer() == 1:
                m = agent1.predict(state)
            else:
                m = agent2.predict(state)
            if verbose: print("Best Move: " + str(m) + "\n")
            state.DoMove(m)

            if state.HasWinning(): break
    win1 = 0
    win2 = 0 
    draw = 0
    for _ in tqdm(range(test_game_number), desc="Playing games"):
        while (state.GetMoves() != []):
            if verbose:
                print(str(state))
            if state.LastPlayer() == 1:
                m = agent1.predict(state)
            else:
                m = agent2.predict(state)
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
        if not winning:
            draw += 1
        elif winner == 1:
            win1 += 1
        else:
            win2 += 1
    return (win1, win2, draw)