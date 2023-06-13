#!/~/dev/SI/prac4/env/bin python3
from random import choice
from reversi_bitboard import ReversiState
from operator import itemgetter

class Player:
    
    DEPTH = 3
    TREE_DEPTH_SORT = 10 
    
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
                return float('inf'), None
            elif res < 0:
                return float('-inf'), None
            else:
                return 0, None

        if depth == 0:
            return self.eval(state), None
        
        moves = state.moves_list()
        
        if self.TREE_DEPTH_SORT > 0:
            
            if max_player:
                moves = [(move, -self.eval(state.move_new_state(move))) for move in moves]
                moves.sort(key = itemgetter(1))
            else:
                moves = [(move, self.eval(state.move_new_state(move))) for move in moves]
                moves.sort(key = itemgetter(1))
            moves = [x[0] for x in moves]
        
        if max_player:
            value, next_move = float('-inf'), None   
            for move in moves:
                child = state.move_new_state(move)
                child_value, unused_move = self.alpha_beta(child, depth-1, alpha, beta, False)

                if child_value >= value:
                    value = child_value
                    next_move = move

                alpha = max(value, alpha)
                
                if value >= beta:
                    break

        else:
            value, next_move = float('inf'), None
            for move in moves:
                child = state.move_new_state(move)
                child_value, unused_move = self.alpha_beta(child, depth-1, alpha, beta, True)

                if child_value <= value:
                    value = child_value
                    next_move = move

                beta = min(value, beta)

                if value <= alpha:
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
            while not self.state.terminal():
                move = None
                if self.my_player == to_move:
                    depth = self.DEPTH
                    # if self.length <= 20:
                    #      depth = 3
                    # elif self.length >= 54:
                    #      depth = 6
                    unused_value, move = self.alpha_beta(self.state, depth, float('-inf'), float('inf'), self.my_player)
                    Player.TREE_DEPTH_SORT -= 1
                else:
                    moves = self.state.moves_list()
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
    print(player.simulate(100))