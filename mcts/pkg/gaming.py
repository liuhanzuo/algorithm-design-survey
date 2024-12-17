import pkg.tictactoe as tictactoe
import random
import pkg.agents as agents
from tqdm import tqdm
from multiprocessing import Pool
def PlaySingleGame(args):
    verbose, agent1, agent2, random_flag, test = args
    state = tictactoe.TicTacToe()
    if random_flag:
        state.SetLastPlayer(random.choice([1, 2]))
    win1 = 0
    win2 = 0
    draw = 0
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
    if test:
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
def PlayGame(args):
    train_game_number, test_game_number, verbose, itermax1, itermax2, selection1, selection2 = args
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    assert selection1 is not None
    assert selection2 is not None
    agent1 = agents.Agent(itermax=itermax1, verbose=False, selection=selection1)
    agent2 = agents.Agent(itermax=itermax2, verbose=False, selection=selection2)
    pool = Pool(processes=32)
    for result in tqdm(pool.imap_unordered(PlaySingleGame, [(verbose, agent1, agent2, True, False)] * train_game_number),
         total=train_game_number):
        pass
        
    win1 = 0
    win2 = 0 
    draw = 0
    for result in tqdm(pool.imap_unordered(PlaySingleGame, [(verbose, agent1, agent2, False, True)] * test_game_number),
            total=test_game_number):
        win1 += result[0]
        win2 += result[1]
        draw += result[2]
    return (win1, win2, draw)

def PlayRandomGame(args):
    train_game_number, test_game_number, verbose, itermax1, itermax2, selection1, selection2 = args
    """ Play a sample game between two UCT players where each player gets a different number
        of UCT iterations (= simulations = tree nodes).
    """
    assert selection1 is not None
    assert selection2 is not None
    agent1 = agents.Agent(itermax=itermax1, verbose=False, selection=selection1)
    agent2 = agents.Agent(itermax=itermax2, verbose=False, selection=selection2)
    pool = Pool(processes=32)
    for result in tqdm(pool.imap_unordered(PlaySingleGame, [(verbose, agent1, agent2, True, False)] * train_game_number),
         total=train_game_number):
        pass
        
    win1 = 0
    win2 = 0 
    draw = 0
    for result in tqdm(pool.imap_unordered(PlaySingleGame, [(verbose, agent1, agent2, True, True)] * test_game_number),
            total=test_game_number):
        win1 += result[0]
        win2 += result[1]
        draw += result[2]
    return (win1, win2, draw)