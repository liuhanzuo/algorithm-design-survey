import random
import numpy as np
from multiprocessing import Pool
import itertools
from tqdm import tqdm
import pandas as pd
import matplotlib.pyplot as plt
import pkg.gaming as gaming
import os
def main(selection1 = None, selection2 = None):
    """ Play a several game to the end using UCT for both players.
    """


    number_of_games = 1000

    results_list = []
    # processing
    win_rate1 = []
    win_rate2 = []
    draw_rate = []
    for j in range(1, 20):
        args=([(number_of_games, number_of_games, False, 10 * j, 80, selection1, selection2)])
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
    plt.savefig(f'figs/80/{selection1} vs {selection2}1.png')
    win_rate1 = []
    win_rate2 = []
    draw_rate = []
    for j in range(1, 20):
        args=([(number_of_games, number_of_games, False, 80, 10*j, selection2, selection1)])
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
    plt.savefig(f'figs/80/{selection2} vs {selection1}1.png')
    win_rate1 = []
    win_rate2 = []
    draw_rate = []
    for j in range(1, 20):
        args=([(number_of_games, number_of_games, False, 10 * j, 80, selection1, selection2)])
        win1, win2, draw = gaming.PlayRandomGame(args[0])
        print("Player1 wins: %2.2f%%" % (win1/number_of_games*100))
        print("Player2 wins: %2.2f%%" % (win2/number_of_games*100))
        print("Draws: %2.2f%%" % (draw/number_of_games*100))
        win_rate1.append(win1/number_of_games*100)
        win_rate2.append(win2/number_of_games*100)
        draw_rate.append(draw/number_of_games*100)
        print(win1, win2, draw)
    plt.clf()
    plt.plot(range(1, 20), win_rate1, label=f'{selection1} first Win Rate')
    plt.plot(range(1, 20), win_rate2, label=f'{selection2} second Win Rate')
    plt.plot(range(1, 20), draw_rate, label='Draw Rate')
    plt.xlabel('Iteration Multiplier')
    plt.ylabel('Win Rate (%)')
    plt.title(f'{selection1} vs {selection2}')
    plt.legend()
    plt.savefig(f'figs/80/{selection1} vs {selection2}2.png')
def playagainst(selection1 = None, selection2 = None, filename = None, epochs = 0):
    """ Play a several game to the end using UCT for both players.
    """

    number_of_games = 10000
    args=([(number_of_games, number_of_games, False, epochs, epochs, selection1, selection2)])
    win1, win2, draw = gaming.PlayRandomGame(args[0])
    with open (filename, 'a') as f:
        f.write(f"{selection1} vs {selection2}, {selection1} wins: %2.2f%%\n" % (win1/number_of_games*100))
        f.write(f"{selection1} vs {selection2}, {selection2} wins: %2.2f%%\n" % (win2/number_of_games*100))
        f.write(f"{selection1} vs {selection2}, Draws: %2.2f%%\n" % (draw/number_of_games*100))
        f.write("\n")
    print("Player1 wins: %2.2f%%" % (win1/number_of_games*100))
    print("Player2 wins: %2.2f%%" % (win2/number_of_games*100))
    print("Draws: %2.2f%%" % (draw/number_of_games*100))

if __name__ == "__main__":
    # selections = ["reward"]
    selections = ['UCT', 'UCB1tuned', 'reward', 'visited']
    epoch_list = [20, 40, 60, 80, 100, 120]
    for epochs in epoch_list:
        print(f'Epochs: {epochs}')
        filename = f'figs/csv/results_{epochs}.csv'
        if not os.path.exists(os.path.dirname(filename)):
            os.makedirs(os.path.dirname(filename))
        # playagainst(selections[i], selections[j], filename, epochs)
        # Initialize a DataFrame to store the results
        results_df = pd.DataFrame(columns=['Selection1', 'Selection2', 'WinRate1', 'WinRate2', 'DrawRate'])
        # Populate the DataFrame with the results
        for i in range(len(selections)):
            for j in range(i, len(selections)):
                number_of_games = 10000
                args = [(number_of_games, number_of_games, False, epochs, epochs, selections[i], selections[j])]
                win1, win2, draw = gaming.PlayRandomGame(args[0])
                new_row = pd.DataFrame([{
                    'Selection1': selections[i],
                    'Selection2': selections[j],
                    'WinRate1': win1 / number_of_games * 100,
                    'WinRate2': win2 / number_of_games * 100,
                    'DrawRate': draw / number_of_games * 100
                }])
                results_df = pd.concat([results_df, new_row], ignore_index=True)
        # Print the DataFrame
        print(results_df)
        # Save the DataFrame to a CSV file
        results_df.to_csv(filename, index=False)