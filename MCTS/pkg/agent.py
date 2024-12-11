import random
import math
from pkg.node import Node
from pkg.selection import selectionpolicy
from pkg.tictactoe import TicTacToe
from tqdm import tqdm

class Agent:
    def __init__(self, train="UCT", test="UCT", itermax=80):
        self.train = train
        self.test = test
        self.itermax = itermax

    def policyagent(self, rootstate, verbose=False, selection = "UCT"):
        """ Conduct a UCT search for itermax iterations starting from rootstate.
            Return the best move from the rootstate.
            Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""

        rootnode = Node(state=rootstate)
        sp = selectionpolicy(selection)
        for i in range(self.itermax):
            node = rootnode
            state = rootstate.Clone()

            # Select
            while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
                node = sp.select(node)
                state.DoMove(node.move)

            # Expand
            if node.untriedMoves != []:
                m = random.choice(node.untriedMoves)
                state.DoMove(m)
                node = node.AddChild(m, state)  # add child and descend tree

            # Rollout
            while state.GetMoves() != [] and not state.HasWinning():  # while state is non-terminal
                state.DoMove(random.choice(state.GetMoves()))

            # Backpropagate
            while node != None:  # backpropagate from the expanded node and work back to the root node
                node.Update(state.GetResult(node.playerJustMoved))
                node = node.parentNode

        return sorted(rootnode.childNodes, key=lambda c: c.visits)[-1].move

    def explore_agent(self, rootstate, verbose=False):
        """ Use an exploration-focused selection algorithm. """
        return self.policyagent(rootstate, verbose, selection=self.train)

    def test_agent(self, rootstate, verbose=False):
        """ Use a test-focused selection algorithm. """
        return self.policyagent(rootstate, verbose, selection=self.test)

    def train_agent(self, num_games, selection="beta"):
        """ Train the agent by exploring the states using the specified selection algorithm. """
        self.selection = selection
        for _ in tqdm(range(num_games), desc="Training Progress"):
            # print("Training game: ", _, num_games)
            game = TicTacToe()
            while game.GetMoves() != []:
                move = self.explore_agent(rootstate=game)
                game.DoMove(move)
                if game.HasWinning():
                    break

class AIAgent:
    def __init__(self, train="UCT", test="UCT", itermax=80):
        self.agent = Agent(train, test, itermax)

    def train(self, num_games):
        self.agent.train_agent(num_games=num_games)

    def play(self, game, gui = None, i = None, j = None):
        ai_move = self.agent.test_agent(rootstate=game)
        if game.board[ai_move] == 0:
            game.DoMove(ai_move)
            if gui:
                gui.update_click(ai_move)
            if game.HasWinning():
                if gui:
                    gui.show_winner()
                return True
            elif not game.HasRemainingMove():
                if gui:
                    gui.show_draw()
                return True
        if game.board[ai_move] != 0:
            return "Invalid Move"
        return False
class HumanAgent:
    def __init__(self):
        pass

    def play(self, game, gui, i, j):
        index = i * 3 + j
        if game.board[index] == 0:
            game.DoMove(index)
            gui.update_click(index)
            if game.HasWinning():
                gui.show_winner()
                return True
            elif not game.HasRemainingMove():
                gui.show_draw()
                return True
        if game.board[index] != 0:
            return "Invalid Move"
        return False
class CombinedAgent:
    def __init__(self, train="UCT", test="UCT", itermax=80):
        self.ai_agent = Agent(train, test, itermax)
        self.human_agent = HumanAgent()

    def train(self, num_games):
        self.ai_agent.train_agent(num_games=num_games)

    def play(self, game, gui, i, j):
        if self.ai_agent.play(game, gui, i, j) == "True":
            return True
        human_move= self.human_agent.play(game, gui, i, j)
        while(human_move == "Invalid Move"):
            human_move = self.human_agent.play(game, gui, i, j)
        if human_move == "True":
            return True
        ai_move = self.ai_agent.play(game, gui, i, j)
        while(ai_move == "Invalid Move"):
            ai_move = self.ai_agent.play(game, gui, i, j)
        if ai_move == "True":
            return True
        return False