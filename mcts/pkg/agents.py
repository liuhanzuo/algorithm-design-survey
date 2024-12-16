from pkg.node import Node
import random
class Agent():
    """ Conduct a UCT search for itermax iterations starting from rootstate.
        Return the best move from the rootstate.
        Assumes 2 alternating players (player 1 starts), with game results in the range [0.0, 1.0]."""
    def __init__(self, itermax, verbose=False, selection = None):
        self.itermax = itermax
        self.verbose = verbose
        self.selection = selection
    def predict(self, rootstate):
        rootnode = Node(state=rootstate, selection=self.selection)

        for i in range(self.itermax):
            node = rootnode
            state = rootstate.Clone()

            # Select
            # Initially a node has not child
            while node.untriedMoves == [] and node.childNodes != []:  # node is fully expanded and non-terminal
                node = node.selectchild()
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
        if (self.verbose):
            print(rootnode.TreeToString(0))
            print(rootnode.ChildrenToString())

        return sorted(rootnode.childNodes, key=lambda c: c.value)[-1].move