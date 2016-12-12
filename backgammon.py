from elements import *
from ai_strategies import *
import random

white = 'w'
black = 'b'

class Game():
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
            self.board.value *= 2
            return self.initiate_game()
            
    @classmethod
    def human_interact(cls, board, turn, first = False):
        temp_board = board.copy()
        temp_turn = turn.copy()
        if first:
            if turn.player == white:
                print "\n White won the right to start !"
                print 
            else:
                print "\n Black won the right to start !"
                print
        if turn.player == white:
            new_player = black
        else:
            new_player = white    
        while not turn.is_complete() and not temp_board.is_complete()[0]:
            print temp_board
            print
            nextmove = raw_input('{} PLAYER: what is your next move? (You can still use these dice: {}) | '.format(temp_turn.player.upper(), temp_turn.roll))
            possiblemoves = temp_board.possible_moves(temp_turn)
            if len(possiblemoves) == 0 and nextmove[0].isdigit():
                print 'NO VALID MOVES TO PLAY, MUST FINALIZE'
                continue
            if nextmove.lower() == 'double':
                temp_board.double()
                continue
            elif 'show' in nextmove.lower():
                print 'Potential Moves: '
                possiblemoves = temp_board.possible_moves(temp_turn)
                if len(possiblemoves) == 0:
                    print 'NO VALID MOVES TO PLAY, MUST FINALIZE'
                else:
                    print possiblemoves
                continue
            elif nextmove.lower() == 'reset':
                temp_board = board.copy()
                temp_turn = turn.copy()
                continue
            elif nextmove.lower() == 'finalize' or nextmove.lower() == 'f':
                board = temp_board
                turn = temp_turn
                break
            elif nextmove.lower() in ['quit', 'exit']:
                return 'exit', 'exit'
            nextmove = [int(x) if x.isdigit() else x for x in nextmove.split()]
            possiblemoves = temp_board.possible_moves(temp_turn)
            if all(l == 0 for l in [len(v) for v in possiblemoves.values()]):
                print 'NO VALID MOVES, MUST FINALIZE'
                break
            which = Board.is_in(possiblemoves, nextmove)
            if  which == False:
                print "Invalid Move."
                continue
            else:
                temp_board = temp_board.move(temp_turn.player, *nextmove)
                temp_turn.roll.use(which)
        board = temp_board
        turn = temp_turn
        return board, Turn(new_player, Roll())

    @classmethod
    def computer_interact(cls, board, turn, strat, simple=True, _print=True):
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
            best_moves = all_[maxIndex][0]
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
        #Comment out if want double 
        while next_t.roll.roll in [[1, 1], [2,2], [3,3], [4,4], [5,5], [6,6]]:
            next_t = Turn(enemy, Roll())
        return  board, next_t

    def human_vs_computer_play(self, comp_strat=careful, pickup=False):
        col_human = raw_input('Which color do you want to play with? Enter W or B: ').lower()
        if col_human not in ['w', 'b']:
            print 'Not a valid color ! Game aborted !'
            return
        col_computer = white if col_human == black else black
        if pickup == False:
            turn = self.initiate_game(Roll())
        else:
            turn = self.history[0]
        self.history.append(turn)
        turn = self.initiate_game(Roll())
        if turn.player == col_human:
            print "\n You won the right to start !"
            print 
        else:
            print "\n The Computer won the right to start !"
            print
        while not turn.is_complete() and not self.board.is_complete()[0]:
            if turn.player == col_human:
                self.board, turn = Game.human_interact(self.board, turn, False)
            else:
                if comp_strat.type == True:
                    self.board, turn = Game.computer_interact(self.board, turn, comp_strat, False, _print=True)
                else:
                    self.board, turn = Game.computer_interact(self.board, turn, comp_strat, simple=True, _print=True)
            if turn == 'exit':
                break
        try:
            print 'GAME CONCLUDED, {} wins !'.format(self.board.is_complete()[1])
        except:
            print 'GAME ABORTED.'
    
    def human_vs_human_play(self, pickup=False):
        if pickup == False:
            turn = self.initiate_game(Roll())
        else:
            turn = self.history[0]
        self.history.append(turn)
        k = True
        while not turn.is_complete() and not self.board.is_complete()[0]:
            self.board, turn = self.human_interact(self.board, turn, k)
            k = False
            self.history.append(turn)
            if turn == 'exit':
                break
        try:
            print 'GAME CONCLUDED, {} wins !'.format(self.board.is_complete()[1])
        except:
            print 'GAME ABORTED.'

    def computer_vs_computer_play(self, comp_strat1=careful, comp_strat2=careful, _print=True):
        turn = self.initiate_game(Roll())
        other = white if turn.player == black else black
        strat = {}
        strat[turn.player] = comp_strat1
        strat[other] = comp_strat2
        if _print:
            print "{} Computer won the right to start !".format(turn.player.upper())
            if comp_strat1 == careful:
                print "{} Computer plays carefully!".format(turn.player.upper())
            else:
                print "{} Computer plays aggressively!".format(turn.player.upper())
            if comp_strat2 == careful:
                print "{} Computer plays carefully!".format(other.upper())
            else:
                print "{} Computer plays aggressively!".format(other.upper())
            print
        c=0
        while not turn.is_complete() and not self.board.is_complete()[0]:
            if c%2==0:
                if comp_strat1.type == True:
                    self.board, turn = self.computer_interact(self.board, turn, comp_strat1, False, _print=_print)
                else:
                    self.board, turn = self.computer_interact(self.board, turn, comp_strat1, simple=True, _print=_print)
            else:
                if comp_strat2.type == True:
                    self.board, turn = self.computer_interact(self.board, turn, comp_strat2, False, _print=_print)
                else:
                    self.board, turn = self.computer_interact(self.board, turn, comp_strat2, simple=True, _print=_print)
            while turn.roll.touse[0] == turn.roll.touse[1]:
                turn = Turn(turn.player, Roll())
            if _print:
                print self.board
            self.history.append(turn)
            c+=1
        if _print:
            print 'GAME CONCLUDED, {} ({}) Computer wins !'.format(self.board.is_complete()[1], str(strat[self.board.is_complete()[1][0].lower()]))            
        return self.board.is_complete()[1], strat[self.board.is_complete()[1][0].lower()], self.board.is_complete()[2]


if __name__ == '__main__':
    message = 'For: \n * Human vs Human: enter 1 \n * Human vs Computer: enter 2 \n * Computer vs Computer: enter 3 \n'
    typ = int(raw_input(message))
    if typ == 1:
        Game().human_vs_human_play()
    elif typ == 2:
        stra = raw_input('Do you want an aggressive (A), careful (C), random (R), logically trained (L/LL) or genetically trained (G21/G41) opponent? ')
        if stra.lower() == 'a':
            print 'Aggressive it is ! Here we go !'
            Game().human_vs_computer_play(comp_strat=aggressive)
        elif stra.lower() == 'r':
            print 'Random it is ! Here we go !'
            Game().human_vs_computer_play(comp_strat=random_)
        elif stra.lower() == 'l':
            print 'Logistically trained it is ! Here we go !'
            Game().human_vs_computer_play(comp_strat=logistic)
        elif stra.lower() == 'g21':
            print 'Genetically trained it is ! Here we go !'
            Game().human_vs_computer_play(comp_strat=genetic_21)
        elif stra.lower() == 'g41':
            print 'Genetically trained it is ! Here we go !'
            Game().human_vs_computer_play(comp_strat=genetic_41)
        elif stra.lower() == 'll':
            print 'Logistically with long features trained it is ! Here we go !'
            Game().human_vs_computer_play(comp_strat=logistic_long)
        else:
            print 'Careful it is ! Here we go !'
            Game().human_vs_computer_play()
    else:
        # print 'Not yet implemented ! Come back later !'
        stra1 = raw_input('Do you want the first computer to be aggressive (A), careful (C), random (R), logically trained (L/LL) or genetically trained (G21/G41)? ')
        if stra1.lower() == 'd':
            Game().computer_vs_computer_play()
        else:  
            stra2 = raw_input('How about the second one? ')
            if stra1.lower() == 'a':
                stra1 = aggressive
            elif stra1.lower() == 'r':
                stra1 = random_
            elif stra1.lower() == 'l':
                stra1 = logistic
            elif stra1.lower() == 'll':
                stra1 = logistic_long
            elif stra1.lower() == 'g21':
                stra1 = genetic_21
            elif stra1.lower() == 'g41':
                stra1 = genetic_41
            else:
                stra1 = careful
            if stra2.lower() == 'a':
                stra2 = aggressive
            elif stra2.lower() == 'r':
                stra2 = random_
            elif stra2.lower() == 'l':
                stra2 = logistic
            elif stra2.lower() == 'g21':
                stra2 = genetic_21
            elif stra2.lower() == 'g41':
                stra2 = genetic_41
            else:
                stra2 = careful
            Game().computer_vs_computer_play(stra1, stra2)


