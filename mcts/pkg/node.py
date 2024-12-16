import math
class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
        Crashes if state not specified.
    """

    def __init__(self, move=None, parent=None, state=None, selection=None):
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parentNode = parent  # "None" for the root node
        self.childNodes = []
        self.wins = 0
        self.visits = 0
        self.value = 0.0
        self.untriedMoves = state.GetMoves()  # future child nodes
        # the only part of the state that the Node needs later
        self.playerJustMoved = state.playerJustMoved
        self.selection = selection
    def selectchild(self):
        if self.selection == "UCT":
            return self.UCTSelectChild()
        elif self.selection == "reward":
            return self.rewardSelectChild()
        elif self.selection == "visited":
            return self.visitedSelectChild()
        elif self.selection == "beta":
            return self.betaSelectChild()
        elif self.selection == "UCB1tuned":
            return self.UCB1tunedSelectChild()
        else:
            raise NotImplementedError("Not implemented yet")
    def UCB1tunedSelectChild(self):
        """ Use the UCB1-Tuned formula to select a child node. The UCB1-Tuned formula means to select the point with the highest value.
        """
        def V_j(visits, wins, total_visits):
            mean = sum(wins) / len(wins)
            return sum((w - mean) ** 2 for w in wins) / (len(wins) - 1 + 1e-9) / visits + math.sqrt(2 * math.log(total_visits) / visits)

        def UCB1tunedValue(c, node):
            value = math.log(node.visits) / c.visits * min(0.25, V_j(c.visits, [child.wins for child in node.childNodes], node.visits))
            return float(c.wins) / c.visits + math.sqrt(value)

        s = sorted(self.childNodes, key=lambda c: UCB1tunedValue(c, self))[-1]
        return s
    def UCTSelectChild(self):
        """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
            lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
            exploration versus exploitation.
        """
        s = sorted(self.childNodes, key=lambda c: float(c.wins) /
                   c.visits + math.sqrt(2 * math.log(self.visits) / c.visits))[-1]
        return s
    def rewardSelectChild(self):
        """ Use the reward formula to select a child node. The reward formula means to select the point with the highest value.
        """
        s = sorted(self.childNodes, key=lambda c: c.value)[-1]
        return s
    def visitedSelectChild(self):
        """ Use the visited formula to select a child node. The visited formula means to select the point with the highest number of visits.
        """
        s = sorted(self.childNodes, key=lambda c: c.visits)[-1]
        return s
    def betaSelectChild(self):
        """ Use the beta formula to select a child node. The beta formula means to random explore a point in the tree
            otherwise choose the point with the highest value.
        """
        raise NotImplementedError("Not implemented yet")
        
    def AddChild(self, m, s):
        """ Remove m from untriedMoves and add a new child node for this move.
            Return the added child node
        """
        n = Node(move=m, parent=self, state=s, selection=self.selection)
        self.untriedMoves.remove(m)
        self.childNodes.append(n)
        return n
    def Update(self, result):
        """ Update this node - one additional visit and result additional wins. result must be from the viewpoint of playerJustmoved.
        """
        self.visits += 1
        self.wins += result
        self.value = self.wins / float(self.visits)

    def __repr__(self):
        return "[M:" + str(self.move) + " W/V:" + str(self.wins) + "/" + str(self.visits) + " U:" + str(self.untriedMoves) + "]"

    def TreeToString(self, indent):
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s
