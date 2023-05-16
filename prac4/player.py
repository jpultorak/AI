#!/~/dev/SI/prac4/env/bin python3
import numpy as np
import sys
from reversi_state import ReversiState


class Player:
    DEPTH = 1
    TREE_DEPTH_SORT = 0
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = ReversiState()
        self.my_player = 1
        self.say('RDY')

    def say(self, what):
        sys.stdout.write(what)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def hear(self):
        line = sys.stdin.readline().split()
        return line[0], line[1:]
    
    # todo: move function and eval
    def alpha_beta(self, state, depth, alpha, beta, max_player):
        #print((alpha, beta))
        if state.terminal():
            return state.result(), None
        if depth == 0:
            return self.eval(state), None
        
        moves = state.moves()
        if Player.TREE_DEPTH_SORT > 0:
            mult = 1
            if not max_player:
                mult = -1
            children = [(state.move_new_state(move), move) for move in moves]
            moves = [(mult*self.eval(child_move[0]), child_move[1]) for child_move in children]
            moves.sort()
            #print(moves, file=sys.stderr)
            moves = [x[1] for x in moves]
            
        if max_player:
            value, next_move = -np.inf, None   
            for move in moves:
                child = state.move_new_state(move)
                child_value, unused_move = self.alpha_beta(child, depth-1, alpha, beta, False)
                if child_value > value:
                    value = child_value
                    next_move = move
                alpha = max(value, alpha)
                # cutoff
                if value >= beta:
                    #print("max pruned", file=sys.stderr)
                    break

        else:
            value, next_move = np.inf, None
            for move in moves:
                child = state.move_new_state(move)
                child_value, unused_move = self.alpha_beta(child, depth-1, alpha, beta, True)
                if child_value < value:
                    value = child_value
                    next_move = move
                beta = min(value, beta)
                # cutoff
                if value <= alpha:
                    #print("min pruned", file=sys.stderr)
                    break
        return value, next_move
    
    def eval(self, state):
        coeffs = np.array([1, 4, 25])
        vals = np.array([state.result(), state.move_balance(), state.corners_taken()])
        return np.dot(coeffs, vals)
    
    def loop(self):
        while True:
            cmd, args = self.hear()
            if cmd == 'HEDID':
                unused_move_timeout, unused_game_timeout = args[:2]
                move = tuple((int(m) for m in args[2:]))
                if move == (-1, -1):
                    move = None
                self.state.do_move(move)
            elif cmd == 'ONEMORE':
                self.reset()
                continue
            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
                self.my_player = 0

            value, move = self.alpha_beta(self.state, self.DEPTH, -np.inf, np.inf, self.my_player)
           # print(move, file=sys.stderr)
            if move:
                self.state.do_move(move)
            else:
                self.state.do_move(None)
                move = (-1, -1)
            Player.TREE_DEPTH_SORT -= 1
            self.say('IDO %d %d' % move)
            #self.state.draw()

if __name__ == '__main__':
    player = Player()
    player.loop()