from mcts import playGame
from multiprocessing import Pool
from tqdm import tqdm
import matplotlib.pyplot as plt
def play_game_with_iterations(iteration):
    return playGame(1, verbose=False, iteration=iteration)

if __name__ == "__main__":
    test_iterations = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 200]
    number_of_games = 2000
    total_results1 = []
    total_results2 = []
    for i in test_iterations:
        results_list = []
        # pool = Pool(processes=1)
        # for result in tqdm(pool.imap_unordered(play_game_with_iterations, [i] * number_of_games),
        #                    total=number_of_games):
        #     results_list.append(result)
        # pool.close()
        for result in tqdm(map(play_game_with_iterations, [i] * number_of_games), total=number_of_games):
            results_list.append(result)
        pos = 0
        neg = 0
        player1 = 0
        player2 = 0
        for result in results_list:
            if result[0]:
                pos += 1
                if result[1] == 1:
                    player1 += 1
                elif result[1]:
                    player2 += 1
            else:
                neg += 1

        print("Number of positives: %d / %d" % (pos, number_of_games))
        print("Number of negatives: %d / %d" % (neg, number_of_games))
        print("Player1 wins: %2.2f%%" % (float(player1) / pos * 100))
        print("Player2 wins: %2.2f%%" % (float(player2) / pos * 100))
        total_results1.append(float(player1) / pos * 100)
        total_results2.append(float(player2) / pos * 100)
    plt.plot(test_iterations, total_results1, label='Player 1 Wins')
    plt.plot(test_iterations, total_results2, label='Player 2 Wins')
    plt.xlabel('Iterations')
    plt.ylabel('Win Percentage')
    plt.title('Win Percentage vs Iterations')
    plt.legend()
    plt.grid(True)
    plt.savefig('win_percentage_vs_iterations.png')
    plt.show()