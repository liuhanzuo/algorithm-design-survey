import numpy as np
from random import randint
from collections import defaultdict


class TreeNode:

    def __init__(self, parent=None, pre_pos=None, board=None):
        self.pre_pos = pre_pos 

        self.parent = parent  
        self.children = list() 

        self.not_visit_pos = None 

        self.board = board  

        self.num_of_visit = 0               
        # self.num_of_win = 0                     
        self.num_of_wins = defaultdict(int)  
        # self.uct = 0  

    def fully_expanded(self):
        if self.not_visit_pos is None:   
            self.not_visit_pos = self.board.get_legal_pos()     
        # print('len(self.not_visit_pos):', len(self.not_visit_pos), 'len(self.children):', len(self.children))
        # print(True if (len(self.not_visit_pos) == 0 and len(self.children) != 0) else False)
        return True if (len(self.not_visit_pos) == 0 and len(self.children) != 0) else False
        # return True if len(self.not_visit_pos) == 0 else False

    def pick_univisted(self):
        random_index = randint(0, len(self.not_visit_pos) - 1)     
        # print(len(self.not_visit_pos))
        move_pos = self.not_visit_pos.pop(random_index) 
        # print(len(self.not_visit_pos))

        new_board = self.board.move(move_pos) 
        new_node = TreeNode(parent=self, pre_pos=move_pos, board=new_board)  
        self.children.append(new_node)
        return new_node

    def pick_random(self):
        possible_moves = self.board.get_legal_pos()  
        random_index = randint(0, len(possible_moves) - 1)  
        move_pos = possible_moves[random_index]

        new_board = self.board.move(move_pos)
        new_node = TreeNode(parent=self, pre_pos=move_pos, board=new_board)  
        return new_node

    def non_terminal(self):
        game_result = self.board.game_over(self.pre_pos)
        return game_result

    def num_of_win(self):
        # print(self)
        # print(-self.board.next_player)
        wins = self.num_of_wins[-self.board.next_player]
        loses = self.num_of_wins[self.board.next_player]
        return wins - loses
        # return wins

    def best_uct(self, c_param=1.98):
        uct_of_children = np.array(list([
            (child.num_of_win() / child.num_of_visit) + c_param * np.sqrt(np.log(self.num_of_visit) / child.num_of_visit)
            for child in self.children
        ]))
        best_index = np.argmax(uct_of_children)
        # max_uct = max(uct_of_children)
        # best_index = np.where(uct_of_children == max_uct)     
        # best_index = np.random.choice(best_index[0])       
        return self.children[best_index]
    def best_ucb1tuned(self):
        ucb1tuned_of_children = np.array(list([
            (child.num_of_win() / child.num_of_visit) + np.sqrt(np.log(self.num_of_visit) / child.num_of_visit)*min(0.25, child.num_of_visit/self.num_of_visit+np.sqrt(2*np.log(self.num_of_visit)/child.num_of_visit))
            for child in self.children
        ]))
        best_index = np.argmax(ucb1tuned_of_children)
        return self.children[best_index]
    def best_uct_tuned(self, c_param=1.98, d_param=1):
        uct_of_children = np.array(list([
            (child.num_of_win() / child.num_of_visit) + c_param * np.sqrt(np.log(self.num_of_visit) / child.num_of_visit + d_param * np.var([c.num_of_win() / c.num_of_visit for c in self.children]))
            for child in self.children
        ]))
        max_uct = max(uct_of_children)
        best_index = np.where(uct_of_children == max_uct)     
        best_index = np.random.choice(best_index[0])       
        return self.children[best_index]
    def best_visited(self):
        visit_num_of_children = np.array(list([child.num_of_visit for child in self.children]))
        best_index = np.argmax(visit_num_of_children)
        return self.children[best_index]
    def __str__(self):
        return "pre_pos: {}\t pre_player: {}\t num_of_visit: {}\t num_of_wins: {}"\
            .format(self.pre_pos, self.board.board[self.pre_pos[0], self.pre_pos[1]],
                    self.num_of_visit, dict(self.num_of_wins))
