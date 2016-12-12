import numpy as np
import pickle
from backgammon import *
from elements import *
from tqdm import tqdm
from ai_strategies import *
import random

def generate_new_challenger(champion):
    new_w = champion.asList[:]
    for i in range(len(new_w)):
        new_w[i] += random.uniform(-0.5,0.5)
    return SimpleWeights(new_w, True,'challenger')

def genetic_udpate(init_champion, alpha, rounds, max_champ, max_it, past=None):
    if past is None:
        champions=[init_champion]
        l = len(past)
    else:
        champions = past
        l=0
    it = 0
    n_champs = 0
    killer_tour = 0
    while n_champs<max_champ and it<max_it:
        it+=1
        if it % 25 == 0 and it>0:
            print "{} iterations passed...".format(it)
        challenger = generate_new_challenger(champion)
        res, diff = play_n(champions[-1], challenger, rounds)
        if res == 1:
            continue
        elif res == 0:
#             print "We are getting a new Champion !"
            n_champs+=1
            a = alpha
            if diff >= 4:
                a*=2
                killer_tour+=1
            new_champ_weights = [(1-a)*w[0]+a*w[1] for w in zip(champion.asList, challenger.asList)]
            champions.append(SimpleWeights(new_champ_weights, True, 'champion_{}'.format(n_champs)))
    return champions, float(killer_tour)/(len(champions)-l)