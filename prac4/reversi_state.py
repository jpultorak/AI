#!/~/dev/SI/prac4/env/bin python3
import numpy as np
from copy import deepcopy

class ReversiState:
    M = 8
    CORNERS = {(0, M-1), (0, M-1), (M-1, 0), (M-1, M-1)}
    DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self, state=None):
        if state is not None:
            self.copy_constructor(state)
        else:
            self.default_constructor()
       
        
    def default_constructor(self):
        self.board = self.initial_board()
        self.fields = set()
        # previous move of player 0/1
        self.prev_move = [None, None]
        self.player = 0
        for i in range(self.M):
            for j in range(self.M):
                if self.board[i,j] == -1:
                    self.fields.add((j, i))

    def copy_constructor(self, state):
        self.player = state.player
        self.board = np.copy(state.board)
        self.fields = deepcopy(state.fields)
        self.prev_move = [state.prev_move[0], state.prev_move[1]]
        
    def initial_board(self):
        # -1 -> empty; 1/0 -> player 1/0
        B = np.full((self.M, self.M), -1, dtype=int)
        
        B[3, 3] = 1
        B[4, 4] = 1
        B[3, 4] = 0
        B[4, 3] = 0
        return B

    # Ascii representation of board
    def draw(self):
        print(f"-------------------\nEVAL:{self.eval()}\nTO MOVE:{self.player}")
        for i in range(self.M):
            res = []
            for j in range(self.M):
                b = self.board[i, j]
                if b == -1:
                    res.append('.')
                elif b == 1:
                    res.append('#')
                else:
                    res.append('o')
            print(''.join(res))
        print('')

    # for given player, generate possible moves in given board state
    # if player arg is passed consider his moves regardless of actual state
    def moves(self, player = None):
        if player is None:
            player = self.player
        res = []
        for (x, y) in self.fields:
            if any(self.can_take(x, y, direction, player)
                   for direction in self.DIRS):
                res.append((x, y))
        return res
    
    # checks if player can take opponent's pieces in direction d by placing pawn in (x, y)
    def can_take(self, x, y, d, player = None):
        if player is None:
            player = self.player
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.get(x, y) is not None and self.get(x, y) == 1 - player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.get(x, y) == player

    def get(self, x, y):
        if 0 <= x < self.M and 0 <= y < self.M:
            return self.board[y, x]
        return None

    def do_move(self, move):
        if move is None:
            self.prev_move[self.player] = (-1, 1)
            self.player = 1-self.player
            return

        self.prev_move[self.player] = move

        x, y = move
        x0, y0 = move
        self.board[y, x] = self.player
        self.fields.remove(move)
        for dx, dy in self.DIRS:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.get(x, y) == 1 - self.player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.get(x, y) == self.player:
                for (nx, ny) in to_beat:
                    self.board[ny, nx] = self.player
        
        self.player = 1-self.player

    def move_new_state(self, move):
        copy_state = ReversiState(self)
        copy_state.do_move(move)
        return copy_state
    
    def result(self):
        res1, res0 = 0, 0
        for y in range(self.M):
            for x in range(self.M):
                b = self.board[y, x]
                if b == 0:
                    res0 += 1
                elif b == 1:
                    res1 += 1
        return 100*(res1-res0)/(res1+res0)
    
    def move_balance(self):
        b1, b0 = len(self.moves(1)), len(self.moves(0))
        if b1 + b0 == 0:
            return 0
        return 100*(b1-b0)/(b1+b0)
    
    def corners_taken(self):
        res0, res1 = 0, 0
        for (x, y) in ReversiState.CORNERS:
            val = self.get(x, y)
            if val == 1:
                res1 += 1
            elif val == 0:
                res0 += 1
        if res1+res0 == 0:
            return 0
        return 100*(res1-res0)/(res1 + res0)
    # def eval_stability(self):
    #     stable0 = np.full((8, 8), 0)

    #     for (x, y) in ReversiState.CORNERS:
    #         if self.get(x, y) == 0:
    #             stable0[x, y] = 1
        
    #     for x in range(1, 7):
    #         if self.get(x, 0) == 0 and stable0[x-1, 0] or self.get(x+1, 0) == 
    #     for y in range(8):
    #         for x in range(8):
    #             if self.get(x, y) == 0 and 
    def eval(self):
        coeffs = np.array([1, 2, 15])
        vals = np.array([self.result(), self.move_balance(), self.corners_taken()])
        return np.dot(coeffs, vals)
    
    def terminal(self):
        if not self.fields:
            return True
        if self.prev_move[0] is None or self.prev_move[1]  is None:
            return False
        return self.prev_move[0] == (-1, -1) and self.prev_move[1] == (-1, -1)
    

# if __name__ == '__main__':

#     game = ReversiState()
#     game.draw()
#     game.do_move((2, 3))
#     game.draw()
#     game.do_move((2, 2))
#     game.draw()

