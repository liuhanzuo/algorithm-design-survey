from MCTS import monte_carlo_tree_search
from MCTS import monte_carlo_tree_search_ucb1_tuned
from MCTS import monte_carlo_tree_search_uct_tuned
from MCTS import monte_carlo_tree_search_visited
from MCTS import monte_carlo_tree_search_ucb1

class Human:

    def __init__(self, player=-1):
        self.player = player

    def get_action_pos(self, board):
        try:
            location = input("Your move(please use commas to separate the two index): ")
            if isinstance(location, str) and len(location.split(",")) == 2: 
                move_pos = tuple([int(n, 10) for n in location.split(",")])    
            else:
                move_pos = -1
        except:
            move_pos = -1

        if move_pos == -1 or move_pos not in board.get_legal_pos():
            print("Invalid Move")
            move_pos = self.get_action_pos(board)
        return move_pos

    def action(self, board):
        move_pos = self.get_action_pos(board)
        board = board.move(move_pos)    # 新的棋盘
        return board, move_pos


class UCTAI:
    """AI player"""

    def __init__(self, player=1, mcts_times=None):
        self.player = player
        self.mcts_times = mcts_times

    @staticmethod
    def action(self, board, pre_pos):
        move_pos = monte_carlo_tree_search(board, pre_pos, mcts_times=self.mcts_times)
        board = board.move(move_pos)  # 新的棋盘
        return board, move_pos
class UCB1tunedAI:
    def __init__(self, player=1, mcts_times=None):
        self.player = player
        self.mcts_times = mcts_times

    @staticmethod
    def action(self, board, pre_pos):
        move_pos = monte_carlo_tree_search_ucb1_tuned(board, pre_pos, mcts_times=self.mcts_times)
        board = board.move(move_pos)  # 新的棋盘
        return board, move_pos
class UCTtunedAI:
    def __init__(self, player=1, mcts_times=None):
        self.player = player
        self.mcts_times = mcts_times

    @staticmethod
    def action(self, board, pre_pos):
        move_pos = monte_carlo_tree_search_uct_tuned(board, pre_pos, mcts_times=self.mcts_times)
        board = board.move(move_pos)  # 新的棋盘
        return board, move_pos
class visitedAI:
    def __init__(self, player=1, mcts_times=None):
        self.player = player
        self.mcts_times = mcts_times
    
    @staticmethod
    def action(self, board, pre_pos):
        move_pos = monte_carlo_tree_search_visited(board, pre_pos, mcts_times=self.mcts_times)
        board = board.move(move_pos)  # 新的棋盘
        return board, move_pos
class UCB1AI:
    def __init__(self, player=1, mcts_times=None):
        self.player = player
        self.mcts_times = mcts_times

    @staticmethod
    def action(self,board, pre_pos):
        move_pos = monte_carlo_tree_search_ucb1(board, pre_pos, mcts_times=self.mcts_times)
        board = board.move(move_pos)  # 新的棋盘
        return board, move_pos