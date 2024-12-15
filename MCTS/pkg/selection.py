from pkg.node import Node
import random
import math
class selectionpolicy:
    def __init__(self, selection):
        self.selection = selection
    def select(self, node: Node):
        if self.selection == "UCT":
            return UCTSelectChild(node)
        elif self.selection == "reward":
            return rewardSelectChild(node)
        elif self.selection == "visited":
            return visitedSelectChild(node)
        elif self.selection == "beta":
            return betaSelectChild(node)
        elif self.selection == "UCB1tuned":
            return UCB1tunedSelectChild(node)
        else:
            raise NotImplementedError("Not implemented yet")
def UCTSelectChild(node: Node):
    """ Use the UCB1 formula to select a child node. Often a constant UCTK is applied so we have
        lambda c: c.wins/c.visits + UCTK * sqrt(2*log(self.visits)/c.visits to vary the amount of
        exploration versus exploitation.
    """
    s = sorted(node.childNodes, key=lambda c: float(c.wins) /
               c.visits + math.sqrt(2 * math.log(node.visits) / c.visits))[-1]
    return s
def V_j(n_j, X_j, node_visits):
    mean_X_j = sum(X_j) / n_j
    return (0.5 * sum(x**2 for x in X_j) - mean_X_j**2 + math.sqrt(2 * math.log(node_visits) / n_j))

def UCB1tunedSelectChild(node: Node):
        """ Use the UCB1-Tuned formula to select a child node. The UCB1-Tuned formula means to select the point with the highest value.
        """
        def UCB1tunedValue(c, node):
            value = math.log(node.visits) / c.visits * 8* min(0.25, V_j(c.visits, [child.wins for child in node.childNodes], node.visits))
            return float(c.wins) / c.visits + math.sqrt(max(0, value))
        s = sorted(node.childNodes, key=lambda c: UCB1tunedValue(c, node))[-1]
        return s
def rewardSelectChild(node: Node):
        """ Use the reward formula to select a child node. The reward formula means to select the point with the highest value.
        """
        s = sorted(node.childNodes, key=lambda c: c.value)[-1]
        return s
def visitedSelectChild(node: Node):
        """ Use the visited formula to select a child node. The visited formula means to select the point with the highest number of visits.
        """
        s = sorted(node.childNodes, key=lambda c: c.visits)[-1]
        return s
def betaSelectChild(node: Node, beta=0.1):
        """ Use the beta formula to select a child node. The beta formula means to random explore a point in the tree
            otherwise choose the point with the highest value.
        """
        if random.random() < beta:
            s = random.choice(node.childNodes)
        else:
            s = sorted(node.childNodes, key=lambda c: c.value)[-1]
        return s