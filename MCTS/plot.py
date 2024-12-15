from mcts import playGame
from tqdm import tqdm
import pkg.agent as agent
import matplotlib.pyplot as plt

if __name__ == "__main__":
    number_of_games = 1000
    agent1 = agent.AIAgent(train="reward", test="reward", itermax=80)
    agent1.train(1000)
    test_iterations = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120]

    total_results1 = []
    total_results2 = []
    total_results3 = []
    for iteration in test_iterations:
        agent2 = agent.AIAgent(train="UCB1tuned", test="reward", itermax=iteration)
        agent2.train(1000)
        results = []
        for _ in tqdm(range(number_of_games), desc="Playing Progress"):
            results.append(playGame(agent1=agent1, agent2=agent2)[1])
        player1_wins = sum(1 for result in results if result == 1)
        player2_wins = sum(1 for result in results if result == 2)
        draw = sum(1 for result in results if result == None)
        total_results1.append(player1_wins / number_of_games * 100)
        total_results2.append(player2_wins / number_of_games * 100)
        total_results3.append(draw / number_of_games * 100)
        print("player1 wins: %d / %d" % (player1_wins, number_of_games))
        print("player2 wins: %d / %d" % (player2_wins, number_of_games))
        print("draw: %d / %d" % (draw, number_of_games)) 
    plt.plot(test_iterations, total_results1, label='Player 1 Wins')
    plt.plot(test_iterations, total_results2, label='Player 2 Wins')
    plt.plot(test_iterations, total_results3, label='Draw')
    plt.xlabel('Iterations')
    plt.ylabel('Win Percentage')
    plt.title('Win Percentage vs Iterations') 
    plt.legend()
    plt.grid(True)
    plt.savefig('reward_UCB1tuned.png')
    plt.show()