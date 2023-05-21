#!/~/dev/SI/prac4/env/bin python3
import numpy as np
# from bitarray import bitarray
# from copy import deepcopy

class ReversiState:
    M = 8
    CORNERS = {(0, M-1), (0, M-1), (M-1, 0), (M-1, M-1)}
    DIRS = [(0, 1), (1, 0), (-1, 0), (0, -1),
            (1, 1), (-1, -1), (1, -1), (-1, 1)]

    def __init__(self):
        self.default_constructor()
           
    def default_constructor(self):
        self.board = self.initial_board()
        self.fields = set()
        # previous moves, and directions in which it took oponent's pieces
        self.prev_moves = []
        self.player = 0
        for i in range(self.M):
            for j in range(self.M):
                if self.board[i,j] == -1:
                    self.fields.add((j, i))
       
    def initial_board(self):
        # -1 -> empty; 1/0 -> player 1/0
        B = np.full((self.M+1, self.M+1), -1, dtype=int)
        
        B[3, 3] = 1
        B[4, 4] = 1
        B[3, 4] = 0
        B[4, 3] = 0
        return B

    # Ascii representation of board
    def draw(self, verbose = 1):
        if verbose >= 2:
           print(f"-------------------\nMoves:{self.moves()}\nfields:{self.fields}")
        if verbose >= 1:
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
            for direction in self.DIRS:
                if self.can_take(x, y, direction, player):
                    res.append((x, y))
                    break
        return res
    
    # checks if player can take opponent's pieces in direction d by placing pawn in (x, y)
    def can_take(self, x, y, d, player = None):
        if player is None:
            player = self.player
        dx, dy = d
        x += dx
        y += dy
        cnt = 0
        while self.board[y, x] == 1 - player:
            x += dx
            y += dy
            cnt += 1
        return cnt > 0 and self.board[y, x] == player

    def do_move(self, move):
        
        if move is None:
            self.prev_moves.append((None, None))
            self.player = 1-self.player
            return

        move_desc = []
        x, y = move
        x0, y0 = move
        self.board[y, x] = self.player
        self.fields.remove(move)
        for dx, dy in self.DIRS:
            x, y = x0, y0
            to_beat = []
            x += dx
            y += dy
            while self.board[y, x] == 1 - self.player:
                to_beat.append((x, y))
                x += dx
                y += dy
            if self.board[y, x] == self.player and to_beat:
                move_desc.append(((dx, dy), to_beat[-1]))
                for (nx, ny) in to_beat:
                    self.board[ny, nx] = self.player

        self.prev_moves.append((move, move_desc))
        self.player = 1-self.player

    def undo_move(self):
        if not self.prev_moves:
            return
        prev_move, desc = self.prev_moves[-1]
        if prev_move is None:
            return

        self.fields.add(prev_move)
        
        x, y = prev_move
        self.board[y, x] = -1
        x0, y0 = prev_move
        # need to remember that player who played last move is 1-self.player
        for dir, last in desc:           
            dx, dy = dir
            x, y = x0, y0
            x += dx
            y += dy
            while (x, y) != last:
                self.board[y, x] = self.player
                x += dx
                y += dy
            self.board[last[1], last[0]] = self.player
        self.prev_moves.pop()
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
            val = self.board[y, x]
            if val == 1:
                res1 += 1
            elif val == 0:
                res0 += 1
        if res1+res0 == 0:
            return 0
        return 100*(res1-res0)/(res1 + res0) 
    
    def frontiers(self):
        res1, res0 = 0, 0
        for y in range(self.M):
            for x in range(self.M):
                b = self.board[y, x]
                if b == -1:
                    continue
                for (dx, dy) in self.DIRS:
                    bb = self.board[y+dy, x+dx]
                    if bb == -1:
                        if b == 0:
                            res0 += 1
                        elif b == 1:
                            res1 += 1
                        break
        return 100*(res1-res0)/(res1+res0)
    
    def eval(self):
        a1 = -1
        a2 = 10
        a3 = 100
        a4 = 10
        length = len(self.prev_moves)
        # early game
        if length <= 20:
            a1 = 2*(length - 21)
            
        elif 45 <= length:
            a2 = 5
            a4 = 5
        elif 55 <= length:
            a2 = 1
            a3 = 10
        elif 58 <= length:
            a1 = 100
            a2 = a3 = a4 = 1

        return a1*self.result() +  a2*self.move_balance() + a3*self.corners_taken()  + a4*self.frontiers()
    
    def terminal(self):
        if not self.fields:
            return True
        if len(self.prev_moves) < 2:
            return False
        return self.prev_moves[-1][0] is None and self.prev_moves[-2][0] is None
    

if __name__ == '__main__':

    game = ReversiState()
    game.draw()
    game.do_move((2, 3))
    game.draw()
    game.do_move((2, 2))
    game.draw()
    game.do_move((3, 2))
    game.draw()
    game.do_move((4, 2))
    game.draw()
    game.undo_move()
    game.draw()
#     game.do_move((2, 2))
#     game.draw()

