import numpy as np

from Node import TreeNode

mcts_times = 100    # MCTS次数


def monte_carlo_tree_search(board, pre_pos):
    root = TreeNode(board=board, pre_pos=pre_pos)    
    for i in range(mcts_times):     
        leaf = traverse(root)  
        simulation_result = rollout(leaf)   
        backpropagate(leaf, simulation_result)  
    return best_child(root).pre_pos


def monte_carlo_tree_search_ucb1_tuned(board, pre_pos):
    root = TreeNode(board=board, pre_pos=pre_pos)    
    for i in range(mcts_times):    
        leaf = traverse_ucb1_tuned(root)  
        simulation_result = rollout(leaf)   
        backpropagate(leaf, simulation_result)
    return best_child_ucb1_tuned(root).pre_pos
def monte_carlo_tree_search_uct_tuned(board, pre_pos):
    root = TreeNode(board=board, pre_pos=pre_pos)    
    for i in range(mcts_times):    
        leaf = traverse_uct_tuned(root)  
        simulation_result = rollout(leaf)   
        backpropagate(leaf, simulation_result)
    return best_child(root).pre_pos
def monte_carlo_tree_search_visited(board, pre_pos):
    root = TreeNode(board=board, pre_pos=pre_pos)    
    for i in range(mcts_times):    
        leaf = traverse_visited(root)  
        simulation_result = rollout(leaf)   
        backpropagate(leaf, simulation_result)
    return best_child(root).pre_pos

def traverse(node):
    """
    层次遍历该结点及其子结点，遇到叶子结点，遇到未完全扩展的结点则对其进行扩展
    :param node: 某一结点
    :return:
    """
    while node.fully_expanded():    
        node = node.best_uct()
    if node.non_terminal() is not None:     
        return node
    else:   
        return node.pick_univisted()   
def traverse_ucb1_tuned(node):
    while node.fully_expanded():    
        node = node.best_ucb1tuned()
    if node.non_terminal() is not None:     
        return node
    else:   
        return node.pick_univisted()   
def traverse_uct_tuned(node):
    while node.fully_expanded():    
        node = node.best_uct_tuned()
    if node.non_terminal() is not None:     
        return node
    else:   
        return node.pick_univisted()
def traverse_visited(node):
    while node.fully_expanded():    
        node = node.best_visited()
    if node.non_terminal() is not None:     
        return node
    else:   
        return node.pick_univisted()


def rollout(node):
    while True:
        game_result = node.non_terminal()
        if game_result is None:     
            node = rollout_policy(node)
        else:       
            break
    if game_result == 'win' and -node.board.next_player == 1:  
        return 1      
    elif game_result == 'win':     
        return -1      
    else:  
        return 0


def rollout_policy(node):
    return node.pick_random()    


def backpropagate(node, result):
    node.num_of_visit += 1
    node.num_of_wins[result] += 1
    if node.parent:  
        backpropagate(node.parent, result)


def best_child(node):
    visit_num_of_children = np.array(list([child.num_of_visit for child in node.children]))
    best_index = np.argmax(visit_num_of_children) 
    node = node.children[best_index]
    return node

def best_child_ucb1_tuned(node):
    visit_num_of_children = np.array(list([child.num_of_visit for child in node.children]))
    total_visits = np.sum(visit_num_of_children)
    best_index = np.argmax([
        (child.num_of_wins[1] / child.num_of_visit) + 
        np.sqrt((np.log(total_visits) / child.num_of_visit) * 
        min(0.25, (np.var([child.num_of_wins[1] for child in node.children]) + np.sqrt(2 * np.log(total_visits) / child.num_of_visit))))
        for child in node.children
    ])
    node = node.children[best_index]
    return node
