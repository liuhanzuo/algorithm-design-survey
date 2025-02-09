from Board import Board
from Players import Human, UCB1tunedAI, UCTAI, visitedAI, UCTtunedAI, UCB1AI

from datetime import datetime
from tqdm import tqdm
from multiprocessing import Pool
import matplotlib.pyplot as plt

class Game:

    def __init__(self):
        self.board = Board()    # 初始棋盘(黑子先手)

    def graphic(self):
        """绘制棋盘"""
        width, height = self.board.size, self.board.size       # 棋盘大小

        print("   黑子(-1) 用 X 表示\t\t\t白子(1) 用 O 表示\n")

        for x in range(width):      # 打印行坐标
            print("{0:8}".format(x), end='')

        print('\r\n')
        for i in range(height):
            print("{0:4d}".format(i), end='')
            for j in range(width):
                if self.board.board[i, j] == -1:
                    print('X'.center(8), end='')
                elif self.board.board[i, j] == 1:
                    print('O'.center(8), end='')
                else:
                    print('-'.center(8), end='')
            print('\r\n\r\n')

    def start_play(self):
        human, ai = Human(), UCB1tunedAI()
        self.graphic()

        while True:

            self.board, move_pos = human.action(self.board)
            print(move_pos)
            game_result = self.board.game_over(move_pos)

            self.graphic()
            if game_result == 'win' or game_result == 'tie':    # 游戏结束
                print('黑子落棋: {}, 黑子(-1)胜利！游戏结束！'.format(move_pos)) if game_result == 'win' \
                    else print('黑子落棋: {}, 平局！游戏结束！'.format(move_pos))
                break
            else:
                print('黑子落棋: {}, 未分胜负, 游戏继续！'.format(move_pos))

            # start_time = datetime.now()
            self.board, move_pos = ai.action(self.board, move_pos)
            print(move_pos)
            # print(datetime.now() - start_time)
            game_result = self.board.game_over(move_pos)
            self.graphic()
            if game_result == 'win' or game_result == 'tie':    # 游戏结束
                print('白子落棋: {}, 白子(1)胜利！游戏结束！'.format(move_pos)) if game_result == 'win' \
                    else print('白子落棋: {}, 平局！游戏结束！'.format(move_pos))
                break
            else:
                print('白子落棋: {}, 未分胜负, 游戏继续！'.format(move_pos))

def AIvsAI(args):
    ai1, ai2 = args
    # ai1, ai2 = UCTtunedAI(), UCTAI()
    board = Board()
    flag = None
    while True:
        board, move_pos = ai1.action(ai1, board, None)
        # print(move_pos)
        game_result = board.game_over(move_pos)
        # if game_result == 'win' or game_result == 'tie':    # 游戏结束
        #     print('黑子落棋: {}, 黑子(-1)胜利！游戏结束！'.format(move_pos)) if game_result == 'win' \
        #         else print('黑子落棋: {}, 平局！游戏结束！'.format(move_pos))
        #     break
        # else:
        #     print('黑子落棋: {}, 未分胜负, 游戏继续！'.format(move_pos))
        if game_result == "win":
            flag = "win"
            break
        if game_result == "tie":
            flag = "tie"
            break
        board, move_pos = ai2.action(ai2,board, move_pos)
        # print(move_pos)
        game_result = board.game_over(move_pos)
        # if game_result == 'win' or game_result == 'tie':    # 游戏结束
        #     print('白子落棋: {}, 白子(1)胜利！游戏结束！'.format(move_pos)) if game_result == 'win' \
        #         else print('白子落棋: {}, 平局！游戏结束！'.format(move_pos))
        #     break
        # else:
        #     print('白子落棋: {}, 未分胜负, 游戏继续！'.format(move_pos))
        if game_result == "win":
            flag = "lose"
            break
        if game_result == "tie":
            flag = "tie"
            break
    return flag
if __name__ == "__main__":
    game = Game()
    # game.start_play()
    playepoch = 1000
    
    pool = Pool()
    final_win = []
    final_lose = []
    final_draw = []
    mcts_epochs = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000]
    for mcts_epoch in mcts_epochs:
        ai1=UCB1AI(mcts_times=mcts_epoch)
        ai2=UCTAI(mcts_times=mcts_epoch)
        results = {"win": 0, "tie": 0, "lose": 0}
        args = [(ai1, ai2) for _ in range(playepoch)]
        for result in tqdm(pool.imap_unordered(AIvsAI, args), total=playepoch, desc=f"{ai1} vs {ai2}, {playepoch} games"):
            results[result] += 1
        print(f"Results after {playepoch} games between {ai1} and {ai2}: {results}")
        with open("result.txt", "a") as f:
            f.write(f"Results after {playepoch} games between {ai1} and {ai2}: {results}\n")
        final_win.append(results["win"]/playepoch)
        final_lose.append(results["lose"]/playepoch)
        final_draw.append(results["tie"]/playepoch)


    plt.figure(figsize=(10, 6))
    plt.plot(mcts_epochs, final_win, label='Win Rate', marker='o')
    plt.plot(mcts_epochs, final_lose, label='Lose Rate', marker='o')
    plt.plot(mcts_epochs, final_draw, label='Draw Rate', marker='o')

    plt.xlabel('MCTS Epochs')
    plt.ylabel('Rate')
    plt.title('AI vs AI Performance')
    plt.legend()
    plt.grid(True)
    plt.savefig("result.png")
    plt.show()


