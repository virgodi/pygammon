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
        while not turn.is_complete():
            print temp_board
            print
            nextmove = raw_input('{} PLAYER: what is your next move? (You can still use these dice: {}) | '.format(temp_turn.player.upper(), temp_turn.roll))
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
            elif nextmove.lower() == 'finalize':
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
        return board, Turn(new_player, Roll())

    @classmethod
    def computer_interact(cls, board, turn, strat):
        scores = {}
        print 'Computer rolled: ', turn.roll
        col = turn.player
        enemy = white if col == black else black
        if len(turn.roll.touse) == 2:
            for d, ms in board.possible_moves(turn).items():
                for m in ms:
                    temp_turn = turn.copy()
                    temp_turn.roll.use(d)
                    temp_board = board.move(col, *m)
                    poss = temp_board.possible_moves(temp_turn)
                    if all(len(v)>0 for v in poss.values()):
                        for dd, mms in poss.items():
                            for mm in mms:
                                if (tuple(m), tuple(mm)) in scores.keys():
                                    continue
                                temp_final = temp_board.move(col, *mm)
                                scores[(tuple(m), tuple(mm))] = ai_strategies.score(strat, [board.state[col]-temp_final.state[col], temp_final.home[col], 
                                    temp_final.alone[col], temp_final.safe[col], temp_final.prison[enemy], temp_final.inhouse[col]])
                    else:
                        scores[(tuple(m), ' ')] = ai_strategies.score(strat, [board.state[col]-temp_board.state[col], temp_board.home[col], 
                            temp_board.alone[col], temp_board.safe[col], temp_board.prison[enemy], temp_board.inhouse[col]])
        else:
            for m in board.possible_moves(turn).values()[0]:
                for m2 in board.move(black, *m).possible_moves(turn).values()[0]:
                    for m3 in board.move(black, *m).move(black, *m2).possible_moves(turn).values()[0]:
                        for m4 in board.move(black, *m).move(black, *m2).move(black, *m3).possible_moves(turn).values()[0]:
                            temp_board = board.move(black, *m).move(black, *m2).move(black, *m3).move(black, *m4)
                            k = (tuple(m), tuple(m2), tuple(m3), tuple(m4))
                            scores[k] = ai_strategies.score(strat, [board.state[col]-temp_board.state[col], temp_board.home[col], 
                                        temp_board.alone[col], temp_board.safe[col], temp_board.prison[enemy], temp_board.inhouse[col]])
            # pass
        all_ = scores.items()
        values = [x[1] for x in all_]
        maxIndex = values.index(max(values))
        best_moves = all_[maxIndex][0]
        for m in best_moves:
            if m == ' ':
                continue
            else:
                board = board.move(col, *m)
        print '{} Computer played: '.format(col), best_moves
        return  board, Turn(enemy, Roll())

    def human_vs_computer_play(self, pickup=False):
        col_human = raw_input('Which color do you want to play with? ').lower()
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
        while not turn.is_complete():
            if turn.player == col_human:
                self.board, turn = Game.human_interact(self.board, turn, False)
            else:
                self.board, turn = Game.computer_interact(self.board, turn, careful)
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
        while not self.board.is_complete()[0]:
            self.board, turn = Game.human_interact(self.board, turn, k)
            k = False
            self.history.append(turn)
            if turn == 'exit':
                break
        try:
            print 'GAME CONCLUDED, {} wins !'.format(self.board.is_complete()[1])
        except:
            print 'GAME ABORTED.'

if __name__ == '__main__':
    message = 'For: \n * Human vs Human: enter 1 \n * Human vs Computer: enter 2 \n * Computer vs Computer: enter 3 \n'
    typ = int(raw_input(message))
    if typ == 1:
        Game().human_vs_human_play()
    elif typ == 2:
        Game().human_vs_computer_play()
    else:
        Game().computer_vs_computer_play()


