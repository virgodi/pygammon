import numpy as np
import pickle
from backgammon import *
from elements import *
from tqdm import tqdm
from ai_strategies import *
import random

def play_n(champion, challenger, n, show=False):
    champ_score = 0
    chal_score = 0
    while champ_score<n and chal_score<n:
        col, winner_strat, mars = Game().computer_vs_computer_play(champion, challenger, False)
        if winner_strat.name == champion.name:
            if mars:
                champ_score+=2
            else:
                champ_score+=1
        elif winner_strat.name == challenger.name:
            if mars:
                chal_score+=2
            else:
                chal_score+=1
    if show:
        print 'Champ: {}'.format(champ_score)
        print 'Chal: {}'.format(chal_score)
    if champ_score == n:
        return 1, abs(champ_score-chal_score)
    else:
        return 0, abs(champ_score-chal_score)