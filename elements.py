import copy
import random
import numpy

white = 'w'
black = 'b'

def MoveError(Exception):
    pass
def removeListDuplicate(l):
    new_l = []
    for elem in l:
        if elem not in new_l:
            new_l.append(elem)
    return new_l
class Roll():
    def __init__(self, d=None):
        if d is None:
            self.roll = [random.choice(range(1, 7)) for i in range(2)]
        else:
            assert isinstance(d,list), 'Given roll must be parsed as a list.'
            if max(d)>6 or min(d)<1:
                raise Exception('Invalid roll.')
            else:
                self.roll = d
        if self.roll[0] == self.roll[1]:
            self.touse = [self.roll[0] for i in range(4)]
        else:
            self.touse = self.roll[:]
    def use(self, x):
        self.touse.remove(x)
    def __repr__(self):
        return str(self.touse)

class Turn():
    def __init__(self, player, roll):
        self.player = player
        self.roll = roll
        
    def is_complete(self):
        if len(self.roll.touse) == 0:
            return True
        else:
            return False
    def copy(self):
        return copy.deepcopy(self)
    def __repr__(self):
        return "Player: {}, Roll: {}".format(str(self.player), str(self.roll))

class Board():
    def __init__(self, spec=None):
        self.board = dict(zip(range(24),[None for i in range(24)]))
        self.prison = {}
        self.prison[white] = 0
        self.prison[black] = 0
        self.home = {}
        self.home[white] = 0
        self.home[black] = 0
        self.state = {}
        self.state[white] = None
        self.state[black] = None
        self.value = 1
        self.initialise_board(spec)
        self.alone = {}
        self.update_alone()
        self.safe = {}
        self.update_safe()
        self.inhouse = {}
        self.update_inhouse()
    def eval_state(self):
        self.state[white]= 0
        self.state[black] = 0
        for k,v in self.board.items():
            if v and v[0] == white:
                self.state[white] += (k+1)*v[1]      
            elif v and v[0] == black:
                self.state[black] += (24-k)*v[1]
        
    def initialise_board(self, spec):
        if spec is None:
            self.board[5] = [white, 5]
            self.board[7] = [white, 3]
            self.board[12] = [white, 5]
            self.board[23] = [white, 2]
            self.board[0] = [black, 2]
            self.board[11] = [black, 5]
            self.board[16] = [black, 3]
            self.board[18] = [black, 5]
        else:
            for k,v in spec.items():
                self.board[k] = v
        self.eval_state()

    def safe_pieces(self, col):
        enemy = white if col == black else black
        if self.prison[enemy] > 0:
            return 0
        else:
            c = self.home[col]
            if enemy == white:
                min_piece = -1
                for k, v in self.board.iteritems():
                    if v and v[0] == enemy and k>min_piece:
                        min_piece=k
                for k, v in self.board.iteritems():
                    if v and v[0] == col and k>min_piece:
                        c+=v[1]
            else:
                min_piece = 999
                for k, v in self.board.iteritems():
                    if v and v[0] == enemy and k<min_piece:
                        min_piece=k
                for k, v in self.board.iteritems():
                    if v and v[0] == col and k<min_piece:
                        c+=v[1]
            return c

    def update_safe(self):
        self.safe[white] = self.safe_pieces(white)
        self.safe[black] = self.safe_pieces(black)

    def alone_pieces(self, col):
        c = 0
        for v in self.board.values():
            if v and v[0] == col and v[1] == 1:
                c+=1
        return c

    def update_alone(self):
        self.alone[white] = self.alone_pieces(white)
        self.alone[black] = self.alone_pieces(black)

    def is_complete(self):
        if self.home[white] == 15:
            return True, 'White'
        elif self.home[black] == 15:
            return True, 'Black'
        else:
            return False, None
        
    def color_pieces(self, col):
        return [k for k,v in self.board.items() if v and v[0]==col]
    
    def furthest_from_home(self, col):
        if col == white:
            return max([k for k,v in self.board.items() if v and v[0]==white])
        else:
            return min([k for k,v in self.board.items() if v and v[0]==black])
    
    def update_inhouse(self):
        c_w = 0
        c_b = 0
        for k, v in self.board.iteritems():
            if v and v[0] == white and k<6:
                c_w+=v[1]
            elif v and v[0] == black and k>19:
                c_b+=v[1]
        self.inhouse[white]=c_w
        self.inhouse[black]=c_b

    def copy(self):
        new = copy.deepcopy(self)
        return new
    
    def double(self):
        self.value*=2
        
    def pop(self, i):
        if self.board[i][1] > 1:
            self.board[i][1]-=1
        elif self.board[i][1] == 1:
            self.board[i] = None
        else:
            raise Exception('No points to remove.')
    
    def possible_moves(self, turn):
        col = turn.player
        roll = turn.roll.touse
        if len(roll) == 0:
            return []
        poss_moves = {}
        for d in roll:
            poss_moves[d] = []
        if self.prison[col]>0:
            if col == white:
                for d in roll:
                    if self.board[24-d] is None or self.board[24-d][1]<=1 or self.board[24-d][0] == white:
                        poss_moves[d].append(['p', 24-d])
            else:
                for d in roll:
                    if self.board[d-1] is None or self.board[d-1][1]<=1 or self.board[d-1][0] == black:
                        poss_moves[d].append(['p', d-1])
            return poss_moves
        f = self.furthest_from_home(col)
        for d in roll:
            if (col==white and f<=5):
                if f <= d-1:
                    poss_moves[d].append([f, 'h'])
                elif self.board[d-1] and self.board[d-1][0]==col and self.board[d-1][1]>0:
                    poss_moves[d].append([d-1, 'h'])
            elif (col==black and f>=18):
                if f >= 24-d:
                    poss_moves[d].append([f, 'h'])
                elif self.board[24-d] and self.board[24-d][0]==col and self.board[24-d][1]>0:
                    poss_moves[d].append([24-d, 'h'])
            
            pieces = self.color_pieces(col)
            for p in pieces:
                if col == white:
                    if p-d in pieces or (p-d>=0 and (self.board[p-d] is None or self.board[p-d][1]<=1)):
                            poss_moves[d].append([p, p-d])
                if col == black:
                    if p+d in pieces or (p+d<=23 and (self.board[p+d] is None or self.board[p+d][1]<=1)):
                        poss_moves[d].append([p, p+d])
        if len(roll) > 1:
            return self.forward_check(poss_moves, turn)
        else:
            toreturn = {}
            for k, v in poss_moves.iteritems():
                toreturn[k] = removeListDuplicate(v)
            return toreturn
            
    def forward_check(self, possiblemoves, turn):
        inadmissible = {}
        for k, moves in possiblemoves.items():
            for move in moves:
                turn_copy = turn.copy()
                turn_copy.roll.use(k)
                next_moves = self.move(turn.player, *move).possible_moves(turn_copy)
                if len(next_moves.values()[0]) == 0:
                    try:
                        inadmissible[k].append(move)
                    except:
                        inadmissible[k] = [move]
        possiblemoves_copy = copy.deepcopy(possiblemoves) 
        for k in possiblemoves_copy.keys():
            if possiblemoves_copy[k]==[]:
                del possiblemoves_copy[k]
        if inadmissible == possiblemoves_copy:
            if all(len(v)>0 for v in possiblemoves.values()):
                possiblemoves_copy = copy.deepcopy(possiblemoves) 
                max_dice = max(possiblemoves_copy.keys())
                possiblemoves_copy = {key: value for key, value in possiblemoves_copy.items() if key == max_dice}
            toreturn = {}
            for k, v in possiblemoves_copy.iteritems():
                toreturn[k] = removeListDuplicate(v)
            return toreturn
        elif len(inadmissible)>0:
            possiblemoves_copy = copy.deepcopy(possiblemoves) 
            for k, v in inadmissible.items():
                possiblemoves_copy[k] = [x for x in possiblemoves_copy[k] if x not in inadmissible[k]]
            toreturn = {}
            for k, v in possiblemoves_copy.iteritems():
                toreturn[k] = removeListDuplicate(v)
            return toreturn
        else:
            toreturn = {}
            for k, v in possiblemoves.iteritems():
                toreturn[k] = removeListDuplicate(v)
            return toreturn

    @classmethod
    def is_in(cls, possiblemoves, move):
        for k, v in possiblemoves.items():
            if move in v:
                return k
        return False
    
    def move(self, col, src, dst):
        if self.prison[col]>0 and src != 'p':
            raise Exception('Must empty the prison.')
        if src == 'p':
            if self.board[dst] == None or self.board[dst][0] == col:
                new = self.copy()
                new.prison[col]-=1
                if new.board[dst]:
                    new.board[dst][1]+=1
                else:
                    new.board[dst] = [col, 1]
                new.eval_state()
                new.update_safe()
                new.update_alone()
                new.update_inhouse()
                return new
            elif self.board[dst][0] != col and self.board[dst][1] == 1:
                new = self.copy()
                new.prison[new.board[dst][0]] += 1
                new.board[dst] = [col, 1]
                new.eval_state()
                new.update_safe()
                new.update_alone()
                new.update_inhouse()
                return new
            else:
                raise Exception('Cannot free piece at this position.')
        elif dst == 'h':
            if self.prison[col]>0:
                raise Exception('Must empty the prison first.')
            elif (col==white and self.furthest_from_home(col)<=5) or col==black and self.furthest_from_home(col) >=18:
                    new = self.copy()
                    new.home[col]+=1
                    new.pop(src)
                    new.eval_state()
                    new.update_safe()
                    new.update_alone()
                    new.update_inhouse()
                    return new
            else:
                raise Exception('All pieces are not yet in the safe zone.')
        else:
            if self.board[src] is None or src not in self.color_pieces(col):
                raise Exception('No {} piece to move at {}'.format(col, src))
            elif dst<0 or dst>=24:
                raise Exception('Cannot move outside of the board.')
            elif self.board[dst] and self.board[dst][0] != col and self.board[dst][1] >1:
                raise Exception('Cannot move to this position, protected by opponent')
            else:
                new = self.copy()
                if self.board[dst] is None:
                    new.board[dst] = [col, 1]
                elif self.board[dst][0] != col and self.board[dst][1] == 1:
                    new.prison[self.board[dst][0]] += 1
                    new.board[dst] = [col, 1]
                else:
                    new.board[dst][1] += 1
                new.pop(src)
                new.eval_state()
                new.update_safe()
                new.update_alone()
                new.update_inhouse()
                return new
            
    def __repr__(self):
        upp = [[' ' for i in range(12)] for j in range(5)]
        low = [[' ' for i in range(12)] for j in range(5)]
        for k in range(12):
            if self.board[k] is None:
                continue
            else:
                if self.board[k][0] == white:
                    fill = 'o'
                else:
                    fill = 'x'
                if self.board[k][1] <= 5:
                    for i in range(self.board[k][1]):
                        low[i][11-k] = fill
                else:
                    low[0][11-k] = str(self.board[k][1])
                    for i in range(1, 5):
                        low[i][11-k] = fill
                        
        for k in range(12, 24):
            if self.board[k] is None:
                continue
            else:
                if self.board[k][0] == white:
                    fill = 'o'
                else:
                    fill = 'x'
                if self.board[k][1] <= 5:
                    for i in range(self.board[k][1]):
                        upp[i][k-12] = fill
                else:
                    upp[0][k-12] = str(self.board[k][1])
                    for i in range(1, 5):
                        upp[i][k-12] = fill
        low_str = '======================================\n'
        for j in range(4,-1,-1):
            low_str += '|'+'  '.join(low[j][:6])+' | '+'  '.join(low[j][6:])+' |\n'
        low_str += '======================================\n 11 10 9  8  7  6   5  4  3  2  1  0'
        
        upp_str = ' 12 13 14 15 16 17 18 19 20 21 22 23\n======================================\n'
        for j in range(5):
            upp_str += '|'+'  '.join(upp[j][:6])+' | '+'  '.join(upp[j][6:])+' |\n'
        upp_str += '======================================\n'
        
        prison = ['|', 'o']+[' ' for s in range(34)]+['x', '|', '\n']
        prison[15:21] = 'PRISON'
        prison[3] = str(self.prison[white])
        prison[34] = str(self.prison[black])
        prison_str = ''.join(prison)
        
        
        if self.home[white] > 0:
            home_white_str = '\n             EATEN  {}  \n'.format(self.home[white])
            if self.home[black] > 0:
                home_black_str = '            EATEN  {}  \n'.format(self.home[black])
                return '\n'+home_black_str+upp_str+prison_str+low_str+home_white_str
            else:
                 return '\n'+upp_str+prison_str+low_str+home_white_str
        else:
            if self.home[black] > 0:
                home_black_str = '    EATEN  {}  \n'.format(self.home[black])
                return '\n'+home_black_str+upp_str+prison_str+low_str
            else:
                 return '\n'+upp_str+prison_str+low_str