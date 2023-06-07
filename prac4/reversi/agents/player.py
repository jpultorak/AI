#!/~/dev/SI/prac4/env/bin python3
import sys
from reversi_bitboard import ReversiState


class Player:
    DEPTH = 4
    TREE_DEPTH_SORT = 0
    def __init__(self):
        self.reset()

    def reset(self):
        self.state = ReversiState()
        self.my_player = 1
        self.length = 0
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
        
        moves = state.moves()
        # if self.TREE_DEPTH_SORT > 0:
        #     if max_player:
        #         moves.sort(key = cmp_to_key(self.cmp_moves_max))
        #     else:
        #         moves.sort(key = cmp_to_key(self.cmp_moves_min))
        
        if max_player:
            value, next_move = float('-inf'), None   
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
            value, next_move = float('inf'), None
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
    
    def loop(self):
        while True:
            cmd, args = self.hear()
            if cmd == 'HEDID':
                
                unused_move_timeout, unused_game_timeout = args[:2]
                move = tuple((int(m) for m in args[2:]))
                if move == (-1, -1):
                    move = None
                self.state.do_move(move)
                # self.state.draw(2)
            elif cmd == 'ONEMORE':
                self.reset()
                continue
            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
                self.my_player = 0

            value, move = self.alpha_beta(self.state, self.DEPTH, float('-inf'), float('inf'), self.my_player)
            #print(move, file=sys.stderr)
            if move:
                self.state.do_move(move)
            else:
                self.state.do_move(None)
                move = (-1, -1)
            # Player.TREE_DEPTH_SORT -= 1
            self.say('IDO %d %d' % move)
            # self.state.draw(2)
            
if __name__ == '__main__':
    player = Player()
    player.loop()