import numpy as np

num_in_a_row_will_win = 5     # 几子棋


class Board:

    def __init__(self, board=None, size=8, next_player=-1):
        self.size = size 
        self.board = np.zeros((self.size, self.size), int) if board is None else board    

        self.next_player = next_player   

    def get_legal_pos(self):
        indices = np.where(self.board == 0) 
        return list(zip(indices[0], indices[1]))

    def is_move_legal(self, move_pos):

        x, y = move_pos[0], move_pos[1]
        if x < 0 or x > self.size or y < 0 or y > self.size:    
            return False
        if self.board[x, y] != 0:  
            return False

        return True

    def move(self, move_pos):
        if not self.is_move_legal(move_pos):   
            raise ValueError("move {0} on board {1} is not legal". format(move_pos, self.board))
        new_board = Board(board=np.copy(self.board), next_player=-self.next_player)
        new_board.board[move_pos[0], move_pos[1]] = self.next_player    

        return new_board      

    def game_over(self, move_pos):
        if move_pos is None:    
            return None
        if self.board_result(move_pos):    
            return 'win'
        elif len(self.get_legal_pos()) == 0:        
            return 'tie'
        else:     
            return None

    def board_result(self, move_pos):

        x, y = move_pos[0], move_pos[1]
        player = self.board[x, y]   # 落子方
        direction = list([[self.board[i][y] for i in range(self.size)]])  # 纵向是否有五颗连子
        direction.append([self.board[x][j] for j in range(self.size)])  # 横向是否有五颗连子
        direction.append(self.board.diagonal(y - x))  # 该点正对角是否有五颗连子
        direction.append(np.fliplr(self.board).diagonal(self.size - 1 - y - x))  # 该点反对角是否有五颗连子
        for v_list in direction:
            count = 0
            for v in v_list:
                if v == player:
                    count += 1
                    if count == num_in_a_row_will_win:
                        return True     # 该玩家赢下游戏
                else:
                    count = 0
        return False

    def __str__(self):
        return "next_player: {}\nboard:\n{}\n".format(self.next_player, self.board)


if __name__ == '__main__':
    import random
    print(random.randint(0, 0))
    pass

