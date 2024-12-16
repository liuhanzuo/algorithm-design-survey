import random
import numpy as np
from multiprocessing import Pool
import itertools
from tqdm import tqdm
import matplotlib.pyplot as plt
import pkg.gaming as gaming

def main(selection1 = None, selection2 = None):
    """ Play a several game to the end using UCT for both players.
    """


    number_of_games = 1000

    results_list = []
    # processing
    pool = Pool(processes=32)
    win_rate1 = []
    win_rate2 = []
    for j in range(1, 20):
        args=([(i, False, 10 * j, 40, selection1, selection2) for i in range(number_of_games)])
    # args = [(i, False, 10, 40, 'UCT', 'UCT') for i in range(number_of_games)]
        for result in tqdm(pool.imap_unordered(gaming.PlayGame, args),
                        total=number_of_games):
            results_list.append(result)

        # compiling results
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
        print("Player1 wins: %2.2f%%" % (float(player1)/pos*100))
        print("Player2 wins: %2.2f%%" % (float(player2)/pos*100))
        win_rate1.append(float(player1)/pos*100)
        win_rate2.append(float(player2)/pos*100)

    plt.clf()
    plt.plot(range(1, 20), win_rate1, label=f'{selection1} first Win Rate')
    plt.plot(range(1, 20), win_rate2, label=f'{selection2} second Win Rate')
    plt.xlabel('Iteration Multiplier')
    plt.ylabel('Win Rate (%)')
    plt.title(f'{selection1} vs {selection2}')
    plt.legend()
    plt.savefig(f'figs/40/{selection1} vs {selection2}1.png')
    win_rate1 = []
    win_rate2 = []
    for j in range(1, 20):
        args=([(i, False, 40, 10*j, selection2, selection1) for i in range(number_of_games)])
        for result in tqdm(pool.imap_unordered(gaming.PlayGame, args),
                        total=number_of_games):
            results_list.append(result)

        # compiling results
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
        print("Player1 wins: %2.2f%%" % (float(player1)/pos*100))
        print("Player2 wins: %2.2f%%" % (float(player2)/pos*100))
        win_rate1.append(float(player1)/pos*100)
        win_rate2.append(float(player2)/pos*100)

    plt.clf()
    plt.plot(range(1, 20), win_rate1, label=f'{selection2} first Win Rate')
    plt.plot(range(1, 20), win_rate2, label=f'{selection1} second Win Rate')
    plt.xlabel('Iteration Multiplier')
    plt.ylabel('Win Rate (%)')
    plt.title(f'{selection2} vs {selection1}')
    plt.legend()
    plt.savefig(f'figs/40/{selection2} vs {selection1}2.png')
    win_rate1 = []
    win_rate2 = []
    for j in range(1, 20):
        args=([(i, False, 40, 10*j, selection2, selection1) for i in range(number_of_games)])
        for result in tqdm(pool.imap_unordered(gaming.PlayRandomGame, args),
                        total=number_of_games):
            results_list.append(result)

        # compiling results
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
        print("Player1 wins: %2.2f%%" % (float(player1)/pos*100))
        print("Player2 wins: %2.2f%%" % (float(player2)/pos*100))
        win_rate1.append(float(player1)/pos*100)
        win_rate2.append(float(player2)/pos*100)

    plt.clf()
    plt.plot(range(1, 20), win_rate1, label=f'{selection2} first Win Rate')
    plt.plot(range(1, 20), win_rate2, label=f'{selection1} second Win Rate')
    plt.xlabel('Iteration Multiplier')
    plt.ylabel('Win Rate (%)')
    plt.title(f'{selection2} vs {selection1}')
    plt.legend()
    plt.savefig(f'figs/40/{selection2} vs {selection1} random.png')

if __name__ == "__main__":
    selections = ['UCT', 'UCB1tuned', 'reward', 'visited']
    for i in range(len(selections)):
        for j in range(i, len(selections)):
            main(selections[i], selections[j])