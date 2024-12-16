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
    draw_rate = []
    for j in range(1, 20):
        args=([(number_of_games, number_of_games, False, 10 * j, 40, selection1, selection2)])
        win1, win2, draw = gaming.PlayGame(args[0])
        print("Player1 wins: %2.2f%%" % (win1/number_of_games*100))
        print("Player2 wins: %2.2f%%" % (win2/number_of_games*100))
        print("Draws: %2.2f%%" % (draw/number_of_games*100))
        win_rate1.append(win1/number_of_games*100)
        win_rate2.append(win2/number_of_games*100)
        draw_rate.append(draw/number_of_games*100)

    plt.clf()
    plt.plot(range(1, 20), win_rate1, label=f'{selection1} first Win Rate')
    plt.plot(range(1, 20), win_rate2, label=f'{selection2} second Win Rate')
    plt.plot(range(1, 20), draw_rate, label='Draw Rate')
    plt.xlabel('Iteration Multiplier')
    plt.ylabel('Win Rate (%)')
    plt.title(f'{selection1} vs {selection2}')
    plt.legend()
    plt.savefig(f'figs/40/{selection1} vs {selection2}1.png')
    win_rate1 = []
    win_rate2 = []
    draw_rate = []
    for j in range(1, 20):
        args=([(number_of_games, number_of_games, False, 40, 10*j, selection2, selection1)])
        win1, win2, draw = gaming.PlayGame(args[0])
        print("Player1 wins: %2.2f%%" % (win1/number_of_games*100))
        print("Player2 wins: %2.2f%%" % (win2/number_of_games*100))
        print("Draws: %2.2f%%" % (draw/number_of_games*100))
        win_rate1.append(win1/number_of_games*100)
        win_rate2.append(win2/number_of_games*100)
        draw_rate.append(draw/number_of_games*100)
    plt.clf()
    plt.plot(range(1, 20), win_rate1, label=f'{selection2} first Win Rate')
    plt.plot(range(1, 20), win_rate2, label=f'{selection1} second Win Rate')
    plt.plot(range(1, 20), draw_rate, label='Draw Rate')
    plt.xlabel('Iteration Multiplier')
    plt.ylabel('Win Rate (%)')
    plt.title(f'{selection2} vs {selection1}')
    plt.legend()
    plt.savefig(f'figs/40/{selection2} vs {selection1}1.png')
    win_rate1 = []
    win_rate2 = []
    draw_rate = []
    for j in range(1, 20):
        args=([(number_of_games, number_of_games, False, 10 * j, 40, selection1, selection2)])
        win1, win2, draw = gaming.PlayRandomGame(args[0])
        print("Player1 wins: %2.2f%%" % (win1/number_of_games*100))
        print("Player2 wins: %2.2f%%" % (win2/number_of_games*100))
        print("Draws: %2.2f%%" % (draw/number_of_games*100))
        win_rate1.append(win1/number_of_games*100)
        win_rate2.append(win2/number_of_games*100)
        draw_rate.append(draw/number_of_games*100)
    plt.clf()
    plt.plot(range(1, 20), win_rate1, label=f'{selection1} first Win Rate')
    plt.plot(range(1, 20), win_rate2, label=f'{selection2} second Win Rate')
    plt.plot(range(1, 20), draw_rate, label='Draw Rate')
    plt.xlabel('Iteration Multiplier')
    plt.ylabel('Win Rate (%)')
    plt.title(f'{selection1} vs {selection2}')
    plt.legend()
    plt.savefig(f'figs/40/{selection1} vs {selection2}2.png')
if __name__ == "__main__":
    selections = ['UCT', 'UCB1tuned', 'reward', 'visited']
    for i in range(len(selections)):
        for j in range(i, len(selections)):
            main(selections[i], selections[j])