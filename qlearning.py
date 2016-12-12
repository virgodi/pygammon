import numpy as np
import pickle
from elements import *
from tqdm import tqdm
from ai_strategies import *
import random

white = 'w'
black = 'b'

class Q_Game():
    def __init__(self, board=None, turn=None):
        if board:
            self.board = board
        else:
            self.board = Board()
        if turn:
            self.history = [turn]
        else:
            self.history = []
            
    def initiate_game(self, r0=None):
        if r0:
            pass
        else:
            r0 = Roll()
        if r0.roll[0]>r0.roll[1]:
            return Turn(white, r0)
        elif r0.roll[1]>r0.roll[0]:
            return Turn(black, r0)
        else:
#             self.board.value *= 2
            return self.initiate_game()

    @classmethod
    def computer_interact(cls, board, turn, strat, eps=0.9, simple=True, _print=True):
        scores = {}
        if _print:
            print '{} Computer rolled: '.format(turn.player.upper()), turn.roll
        col = turn.player
        enemy = white if col == black else black
        # print board.possible_moves(turn)
        if not all(m==[] for m in board.possible_moves(turn).values()):
            if len(turn.roll.touse) == 2:
                for d, ms in board.possible_moves(turn).items():
                    for m in ms:
                        temp_turn = turn.copy()
                        temp_turn.roll.use(d)
                        temp_board = board.move(col, *m)
                        if temp_board.is_complete()[0]:
                            if _print:
                                print '{} Computer played: '.format(col), m
                            return temp_board, Turn(enemy, Roll())
                        poss = temp_board.possible_moves(temp_turn)
                        if all(len(v)>0 for v in poss.values()):
                            for dd, mms in poss.items():
                                for mm in mms:
                                    if (tuple(m), tuple(mm)) in scores.keys():
                                        continue
                                    temp_final = temp_board.move(col, *mm)
                                    if simple:
                                        scores[(tuple(m), tuple(mm))] = ai_strategies.score(strat, temp_final.get_features(board, col))
                                    else:
                                        scores[(tuple(m), tuple(mm))] = ai_strategies.score(strat, temp_final.feat(board, col))
                        else:
                            if simple:
                                scores[(tuple(m), ' ')] = ai_strategies.score(strat, temp_board.get_features(board, col))
                            else:
                                scores[(tuple(m), ' ')] = ai_strategies.score(strat, temp_board.feat(board, col))
            else:
                poss = board.possible_moves(turn)
                if len(poss)>0 and any(len(x)>0 for x in poss.values()):
                    for m in poss.values()[0]:
                        t = turn.copy()
                        t.roll.use(t.roll.touse[0])
                        if board.move(col, *m).is_complete()[0]:
                            if _print:
                                print '{} Computer played: '.format(col), m
                            return board.move(col, *m), Turn(enemy, Roll())
                        poss1 = board.move(col, *m).possible_moves(t)
                        if len(poss1)>0 and any(len(x)>0 for x in poss1.values()):
                            for m2 in poss1.values()[0]:
                                t1 = turn.copy()
                                t1.roll.use(t1.roll.touse[0])
                                if board.move(col, *m).move(col, *m2).is_complete()[0]:
                                    if _print:
                                        print '{} Computer played: '.format(col), m, m2
                                    return board.move(col, *m).move(col, *m2), Turn(enemy, Roll())
                                poss2 = board.move(col, *m).move(col, *m2).possible_moves(t1)
                                if len(poss2)>0 and any(len(x)>0 for x in poss2.values()):
                                    for m3 in poss2.values()[0]:
                                        t2 = turn.copy()
                                        t2.roll.use(t2.roll.touse[0])
                                        if board.move(col, *m).move(col, *m2).move(col, *m3).is_complete()[0]:
                                            if _print:
                                                print '{} Computer played: '.format(col), m, m2, m3
                                            return board.move(col, *m).move(col, *m2).move(col, *m3), Turn(enemy, Roll())
                                        poss3 = board.move(col, *m).move(col, *m2).move(col, *m3).possible_moves(t2)
                                        if len(poss3)>0 and any(len(x)>0 for x in poss3.values()):
                                            for m4 in poss3.values()[0]:
                                                if board.move(col, *m).move(col, *m2).move(col, *m3).move(col, *m4).is_complete()[0]:
                                                    if _print:
                                                        print '{} Computer played: '.format(col), m, m2, m3, m4
                                                    return board.move(col, *m).move(col, *m2).move(col, *m3).move(col, *m4), Turn(enemy, Roll())
                                                temp_board = board.move(col, *m).move(col, *m2).move(col, *m3).move(col, *m4)
                                                k = (tuple(m), tuple(m2), tuple(m3), tuple(m4))
                                                if simple:
                                                    scores[k] = ai_strategies.score(strat, temp_board.get_features(board, col))
                                                else:
                                                    scores[k] = ai_strategies.score(strat, temp_board.feat(board, col))
                                        else:
                                            temp_board = board.move(col, *m).move(col, *m2).move(col, *m3)
                                            k = (tuple(m), tuple(m2), tuple(m3))
                                            if simple:
                                                scores[k] = ai_strategies.score(strat, temp_board.get_features(board, col))
                                            else:
                                                scores[k] = ai_strategies.score(strat, temp_board.feat(board, col))
                                else:
                                    temp_board = board.move(col, *m).move(col, *m2)
                                    k = (tuple(m), tuple(m2))
                                    if simple:
                                        scores[k] = ai_strategies.score(strat, temp_board.get_features(board, col))
                                    else:
                                        scores[k] = ai_strategies.score(strat, temp_board.feat(board, col))

                        else:
                            temp_board = board.move(col, *m)
                            k = (tuple(m), ' ')
                            if simple:
                                scores[k] = ai_strategies.score(strat, temp_board.get_features(board, col))
                            else:
                                scores[k] = ai_strategies.score(strat, temp_board.feat(board, col))
            all_ = scores.items()
            values = [x[1] for x in all_]
            maxIndex = values.index(max(values))
            if random.uniform(0,1)<eps:
                best_moves = all_[maxIndex][0]
            else:
                best_moves = all_[random.randint(0, len(all_)-1)][0]
            for m in best_moves:
                if m == ' ':
                    continue
                else:
                    board = board.move(col, *m)
            if _print:
                print '{} Computer played: '.format(col.upper()), best_moves
        else:
            if _print:
                print '{} Computer cannot move, your turn !'.format(col)
        next_t = Turn(enemy, Roll())
        while next_t.roll.roll in [[1, 1], [2,2], [3,3], [4,4], [5,5], [6,6]]:
            next_t = Turn(enemy, Roll())
        return  board, next_t
    
    def update(self, comp_strat, og_board, sa, sprime, turn, r, gamma, alpha):
        possible_actions = sprime.get_pairs_moves(turn)
        Qs = []
        f = sa.feat(og_board, turn.player)
        if r == 0:
            if len(possible_actions) == 0:
                return comp_strat
            for action in possible_actions:
                sprime2 = sprime.copy()
                for m in action:
                    if m == ' ':
                        continue
                    else:
                        sprime2 = sprime2.move(turn.player, *m)
                Qs.append(score(comp_strat, sprime2.feat(sprime, turn.player)))
            diff = gamma*max(Qs)-score(comp_strat1, f)
        else:
            diff = r - score(comp_strat, sa.feat(og_board, turn.player))
        new_w = []
        for i in range(len(comp_strat.asList)):
            new_w.append(comp_strat.asList[i]+alpha*diff*f[i])
        return SimpleWeights(new_w, comp_strat.type, comp_strat.name)
    
    def qlearning(self, comp_strat, gamma, alpha, _print=True):
        toimprove = SimpleWeights(comp_strat.asList, True, 'toimprove')
        turn = self.initiate_game(Roll())
#         print turn.player
        other = white if turn.player == black else black
        strat = {}
        strat[turn.player] = comp_strat1 
        strat[other] = comp_strat2
        while True:
            r=0
            shouldBreak = False
#             print turn
            sa, turn = self.computer_interact(self.board, turn, toimprove, 0.9, False, _print=_print)
#             print sa
#             print '****************************************************'
            if sa.is_complete()[0] and sa.is_complete()[1][0].lower() != other:
                if sa.is_complete()[2]:
                    r = 10
                else:
                    r = 5
                shouldBreak = True
            else:
#                 print turn
                sprime, turn = self.computer_interact(sa, turn, comp_strat, 1, False, _print=_print)
#                 print sprime
#                 print '****************************************************'
                if sa.is_complete()[0] and sa.is_complete()[1][0].lower() == other:
                    if sa.is_complete()[2]:
                        r = -10
                    else:
                        r = -5
                    shouldBreak = True
            toimprove = self.update(toimprove, self.board, sa, sprime, turn, r, gamma, alpha)
            if shouldBreak:
                break
            else:
                self.board = sprime
#         print r
        return comp_strat1

def run_qlearning(strat_to_improve, gamma, alpha, max_iteration=100):
    if isinstance(strat_to_improve, list):
        champs = strat_to_improve
    else:
        champs=[strat_to_improve]
    for i in tqdm(range(max_iteration)):
        g = Q_Game()
        champs.append(g.qlearning(champs[-1], gamma, alpha, _print=False))
    return champs