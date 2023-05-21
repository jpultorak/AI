#!/~/dev/SI/prac4/env/bin python3
import numpy as np
from random import choice
from reversi_bitboard import ReversiState

class Player:
    
    DEPTH = 2
    TREE_DEPTH_SORT = 0
    def __init__(self, my_player):
        self.reset(my_player)
        

    def reset(self, my_player):
        self.state = ReversiState()
        self.my_player = my_player
        self.length = 0

    def alpha_beta(self, state, depth, alpha, beta, max_player):
        if state.terminal():
            res = state.result()
            if res > 0:
                return np.inf, None
            elif res < 0:
                return -np.inf, None
            else:
                return 0, None

        if depth == 0:
            return self.eval(state), None
        
        moves = state.moves()
        # if self.TREE_DEPTH_SORT > 0:
        #     if max_player:
        #         moves.sort(key = cmp_to_key(self.cmp_moves_max))
        #     else:
        #         moves.sort(key = cmp_to_key(self.cmp_moves_min))
        
        if max_player:
            value, next_move = -np.inf, None   
            for mv, b in enumerate(moves):
                if not b:
                    continue
                move = state.int_to_coords(mv)
                child = state.move_new_state(move)
                child_value, unused_move = self.alpha_beta(child, depth-1, alpha, beta, False)

                if child_value >= value:
                    value = child_value
                    next_move = move

                alpha = max(value, alpha)
                if value >= beta:
                   #print("max pruned")
                    break

        else:
            value, next_move = np.inf, None
            for mv, b in enumerate(moves):
                if not b:
                    continue
                move = state.int_to_coords(mv)
                child = state.move_new_state(move)
                child_value, unused_move = self.alpha_beta(child, depth-1, alpha, beta, True)

                if child_value <= value:
                    value = child_value
                    next_move = move

                if value <= alpha:
                    #print("min pruned", file=sys.stderr)
                    break
        return value, next_move
    
    def eval(self, state):
        a1 = 1
        a2 = 2
        a3 = 16
        a4 = -1
        # early game
        if self.length <= 20:
            a1 = -2
            
        # # elif 45 <= length<=55:
        # #     a2 = 5

        # # elif 55 <= length:
        # #     a2 = 1
        # #     a3 = 10
        # elif 58 <= self.length:
        #     a1 = 100
        #     a2 = a3 = a4 = 1

        return a1*state.result() +  a2*state.move_balance() + a3*state.corners_taken() + a4*state.frontiers()
    
    
    def simulate(self, N):
        win, draw, lose = 0, 0, 0
        my_player = 1
        for _ in range(0, N):
            
            self.reset(my_player)
            to_move = 0
            # print("NEW GAME")
            # self.state.draw()
            while not self.state.terminal():
                # print(self.length)
                # self.state.draw(verbose=3)
                move = None
                if self.my_player == to_move:
                    depth = self.DEPTH
                    if self.length <= 15:
                         depth = 3
                    elif self.length >= 55:
                         depth = 5
                    unused_value, move = self.alpha_beta(self.state, depth, -np.inf, np.inf, self.my_player)
                else:
                    moves = self.state.moves_from_mask(self.state.moves())
                    if moves:
                        # a, b = tuple(map(int, input().split()))
                        # move = (a, b)
                        move = choice(moves)

                self.state.do_move(move)
                to_move = 1-to_move
                if move is not None:
                    self.length += 1
    
            res = self.state.result()
            if res == 0:
                draw += 1
            elif res > 0 and my_player == 1 or res < 0 and my_player == 0:
                win += 1
            else:
                lose += 1
            # change who goes first
            my_player = 1-my_player
    
        return (win, draw, lose)
        
        
            
if __name__ == '__main__':
    player = Player(1)
    print(player.simulate(1000))