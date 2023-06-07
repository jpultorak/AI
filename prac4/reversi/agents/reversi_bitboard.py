#!/~/dev/SI/prac4/env/bin python3
from bitarray import bitarray, frozenbitarray ,util
from random import choice

class ReversiState:
    M = 8
    CORNERS = {(0, M-1), (0, M-1), (M-1, 0), (M-1, M-1)}
    DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    INIT1 = bitarray('0000000000000000000000000001000000001000000000000000000000000000')
    INIT0 = bitarray('0000000000000000000000000000100000010000000000000000000000000000')
    TOP = bitarray('0000000011111111111111111111111111111111111111111111111111111111')
    DOWN = bitarray('1111111111111111111111111111111111111111111111111111111100000000')
    RIGHT = bitarray('1111111011111110111111101111111011111110111111101111111011111110')
    LEFT = bitarray('0111111101111111011111110111111101111111011111110111111101111111')
    TOPR = bitarray('0000000011111110111111101111111011111110111111101111111011111110')
    TOPL = bitarray('0000000001111111011111110111111101111111011111110111111101111111')
    DOWNL = bitarray('0111111101111111011111110111111101111111011111110111111100000000')
    DOWNR = bitarray('1111111011111110111111101111111011111110111111101111111000000000')
    CORNERSMASK = bitarray('1000000100000000000000000000000000000000000000000000000010000001')

    MASKS = [LEFT, TOPL, TOP, TOPR, RIGHT, DOWNR, DOWN, DOWNL]

    LSHIFTS = [
                0, # Right
                0, # Down-right
                0, # Down
                0, # Down-left
                1, # Left
                9, # Up-left
                8, # Up
                7  # Up-right
    ]
    RSHIFTS = [
                1, # Right
                9, # Down-right
                8, # Down
                7, # Down-left
                0, # Left
                0, # Up-left
                0, # Up
                0  # Up-right
        ]
    
    def __init__(self, state=None):
        if state is None:
            self.default_constructor()
        else:
            self.copy_constructor(state)

    @staticmethod
    def create_copy(state):
        new = ReversiState(state)
        return new
    
    def copy_constructor(self, state):

        self.bits = [None, None]
        self.bits[0], self.bits[1] = state.bits[0].copy(), state.bits[1].copy()
        self.player = state.player

    def default_constructor(self):
        self.bits = [self.INIT0.copy(), self.INIT1.copy()]
        self.player = 0  

    def __hash__(self):
        b0, b1 = frozenbitarray(self.bits[0]), frozenbitarray(self.bits[1])
        return hash((b0, b1, self.player))
    
    def __eq__(self, other):
        return self.player == other.player and self.bits == other.bits
    
    @staticmethod 
    def int_to_coords(x):
        return (x % 8, x // 8)
    
    @staticmethod 
    def coord_to_int(xy):
        return 8*(xy[1]) + xy[0]
    
    def free_fields(self):
        return ~(self.bits[0] | self.bits[1])
    
    def shift(self, mask, dir):
        if dir <= 3:  # rightshift
            return (mask >> self.RSHIFTS[dir]) & self.MASKS[dir]
        return (mask << self.LSHIFTS[dir]) & self.MASKS[dir]
    
    def draw(self, verbose =3):
        def get(x, y):
            
            if self.bits[0][(self.coord_to_int((x, y)))]:
                return 0
            if self.bits[1][(self.coord_to_int((x, y)))]:
                return 1
            return -1
    
        if verbose >= 3:
            print(f"-------------------\n{self.bits[0]}\n{self.bits[1]}")
        if verbose >= 2:
           print(f"Moves:{self.moves_list()}")
        if verbose >= 1:
           print(f"EVAL:{self.eval()}\nTO MOVE:{self.player}")
        for i in range(self.M):
            res = []
            for j in range(self.M):
                b = get(j, i)
                if b == -1:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print(''.join(res))
        print('')
    
    # for given player, generate possible moves as a mask in given board state
    # if player arg is passed consider his moves regardless of actual state
    def moves(self, player = None):
        if player is None:
            player = self.player
        legal_moves = util.zeros(64)
        for dir in range(0, 8):
           
            moves_dir = self.shift(self.bits[player], dir) & self.bits[1-player]
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-player]
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-player]
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-player]
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-player]
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-player]

            legal_moves |= self.shift(moves_dir, dir) & self.free_fields()

        return legal_moves
    
    def print_mask(self, mask):
        print(f"PRINTING MASK {mask}")
        for i in range(self.M):
            res = []
            for j in range(self.M):
                b = mask[self.coord_to_int((j, i))]
                if b == 0:
                    res.append('.')
                else:
                    res.append('#')
            print(''.join(res))
        print('')

    def move_new_state(self, move):
        copy_state = ReversiState(self)
        copy_state.do_move(move)
        return copy_state

    def do_move(self, move):
        if move is None:
            self.player = 1-self.player
            return
        
        move = self.coord_to_int(move)
        new_disk, captured = util.zeros(64), util.zeros(64)
        new_disk[move] = 1
        self.bits[self.player] |= new_disk

        for dir in range(0, 8):
            moves_dir = self.shift(new_disk, dir) & self.bits[1-self.player]
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-self.player]     
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-self.player]    
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-self.player]
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-self.player]
            moves_dir |= self.shift(moves_dir, dir) & self.bits[1-self.player]
            last_disk = self.shift(moves_dir, dir) & self.bits[self.player]
            if last_disk.any():
                captured |= moves_dir
        
        self.bits[self.player] ^= captured
        self.bits[1-self.player] ^= captured
        self.player = 1-self.player
    
    def result(self):
        res1 = self.bits[1].count()
        res0 = self.bits[0].count()
        return 100*(res1-res0)/(res1+res0)
    
    # important assumption: current state is terminal
    def utility(self):
        res1 = self.bits[1].count()
        res0 = self.bits[0].count()
        if res1 > res0:
            return 1
        elif res1 == res0:
            return 0.5
        else:
            return 0
    
    # get children of current state as a list of coords
    def moves_list(self):
        b = self.moves()
        if not b.any() and not self.terminal():  # since state is not terminal, pass is valid move
            return [None]
        return [self.int_to_coords(i) for i in range(64) if b[i]]
   
    def random_child(self):
        moves = self.moves_list()
        if not moves:
            return self.move_new_state(None)
        return self.move_new_state(choice(moves))
    
    def generate_successors(self):
        if self.terminal():
            return tuple()
        moves = self.moves_list()
        return tuple([self.move_new_state(move) for move in moves])
    
    def move_balance(self):
        b0, b1 = self.moves(0).count(), self.moves(1).count()
        if b1 + b0 == 0:
            return 0
        return 100*(b1-b0)/(b1+b0)
    
    def corners_taken(self):
        res0 = (self.bits[0] & self.CORNERSMASK).count()
        res1 = (self.bits[1] & self.CORNERSMASK).count()
        if res1+res0 == 0:
            return 0
        return 100*(res1-res0)/(res1 + res0)
    
    def eval(self):
        return 0.2*self.result() +  2*self.move_balance() + 15*self.corners_taken()
    
    def frontiers(self):
        frontiers0, frontiers1 = util.zeros(64), util.zeros(64)
        empty = self.free_fields()
        for dir in range(8):
            shifted = self.shift(empty, dir)
            frontiers0 |= shifted & self.bits[0]
            frontiers1 |= shifted & self.bits[1]
        frontiers0 &= self.TOPL & self.DOWNR
        frontiers1 &= self.TOPL & self.DOWNR
        f1, f0 = frontiers1.count(), frontiers0.count()
        return 100*(f1-f0)/(f1+f0)
    
    def terminal(self):
        b0, b1 = self.moves(0).count(), self.moves(1).count()
        return b0 + b1 == 0
    

if __name__ == '__main__':
    pass
