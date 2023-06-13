import chess
import chess.engine
from chessboard import display
from time import sleep
from random import randint, random
from functools import cmp_to_key

class Player():
    DEPTH = 2
    MAX_MOVES = 50

    PIECES = [
        chess.PAWN,
        chess.KNIGHT,
        chess.BISHOP,
        chess.ROOK,
        chess.QUEEN,
        chess.KING
    ]

    MVV_LVA = [
    [15, 14, 13, 12, 11, 10], # victim P; attacker: P N B R Q K
    [25, 24, 23, 22, 21, 20], # victim N
    [35, 34, 33, 32, 31, 30], # victim B
    [45, 44, 43, 42, 41, 40], # victim R
    [55, 54, 53, 52, 51, 50], # victim Q
    [0, 0, 0, 0, 0, 0]        # victim K
    ]

    def __init__(self, white, values, mobility):
        self.board = chess.Board()
        self.color = white # 1 if white, 0 otherwise
        self.parameters = {Player.PIECES[i] : values[i] for i in range(6)}
        self.mobility_factor = mobility

    def reset(self, color = False):
        self.board = chess.Board()
        self.color = color

    def __str__(self):
        symbols = ['P', 'N', 'B', 'R', 'Q', 'K']
        s = ''
        for i in range(1, 7):
            s += f'{symbols[i-1]}: {self.parameters[i]} '
        s += f'Mob. fact: {self.mobility_factor}'    
        return s
    
    def move_ordering(self, move1, move2):
        c1, c2 = self.board.is_capture(move1), self.board.is_capture(move2)
        if c1 and c2:

            attacker, victim = self.board.piece_at(move1.from_square).piece_type-1, self.board.piece_at(move1.to_square)
            if victim is None: # exception: en_passant does not 'directly' capture pawn
                victim = chess.PAWN-1
            else:
                victim = victim.piece_type-1
            val1 = Player.MVV_LVA[victim][attacker]

            attacker, victim = self.board.piece_at(move2.from_square).piece_type-1, self.board.piece_at(move2.to_square)
            if victim is None: # exception: en_passant does not 'directly' capture pawn
                victim = chess.PAWN-1
            else:
                victim = victim.piece_type-1
            val2 = Player.MVV_LVA[victim][attacker]
            return val1 - val2

        return c1 - c2
    
    def mobility(self):
        moves = len(list(self.board.legal_moves))
        self.board.turn = 1 - self.board.turn
        moves_1 = len(list(self.board.legal_moves))
        self.board.turn = 1 - self.board.turn
        if self.board.turn:
            return self.mobility_factor*(moves - moves_1)
        return self.mobility_factor*(moves_1 - moves)

    
    def material_balance(self):
        res = 0
        for piece in Player.PIECES:
            mask = self.board.pieces(piece, True)
            res += len(mask)*self.parameters[piece]
            mask = self.board.pieces(piece, False)
            res -= len(mask)*self.parameters[piece]
        return res

    def evaluate(self):

        return self.material_balance() + self.mobility()

    def move_dynamic(self, move):
        if self.board.is_capture(move) or self.board.gives_check(move):
            return True

        if self.board.is_check():
            dynamic = False
            self.board.push(move)
            if not self.board.is_check():
                dynamic = True
            self.board.pop()
            return dynamic
        
    def alpha_beta(self, alpha, beta, depth, max_player, dynamic):
        claim_draw = False
        # if self.board.fullmove_number >= 40:
        #     claim_draw = True

        # 
        outcome = self.board.outcome(claim_draw=claim_draw)
        if outcome is not None: # game has ended
            res = outcome.winner
            if res is None:
                return 0, None
            if res:
                return float('inf'), None

            return float('-inf'), None

        if depth == 0:
            return 10*self.evaluate(), None

        
        moves = list(self.board.legal_moves)
        if dynamic:
            moves = [mv for mv in moves if self.move_dynamic(mv)]
        
        if not moves:
            #print(f"DEPTH: {self.DEPTH - depth}")
            return self.evaluate(), None
        
        next_move = moves[0]
        moves.sort(key=cmp_to_key(self.move_ordering), reverse=True)
        if max_player:
            value = float('-inf')
            for move in moves:

                self.board.push(move)
                child_value, unused_move = self.alpha_beta(alpha, beta, depth-1, False, True)
                self.board.pop()

                if child_value > value:
                    value = child_value
                    next_move = move
                    alpha = max(value, alpha)

                if value >= beta:
                    break
        else:
            value = float('inf')
            for move in moves:

                self.board.push(move)
                child_value, unused_move = self.alpha_beta(alpha, beta, depth-1, True, True)
                self.board.pop()

                if child_value < value:
                    value = child_value
                    next_move = move
                    beta = min(value, beta)

                if value <= alpha:
                    break

        return value, next_move

    def select_move(self):  # max_time in ms
        _val, move = self.alpha_beta(float('-inf'), float('inf'), self.DEPTH, self.color, False)
        #print(_val, move)
        return move

def random_agent():
    vals = [1, -1, -1, -1, -1, 0] # PAWN = 1 KING = 0
    vals[1:5] = [randint(1, 20) for _ in range(4)]
    mobility = random()
    return Player(True, vals, mobility)

def simulate(agent1, agent2):
    agent1.reset()
    agent2.reset()
    global game_board
    agent1.color = 1
    agent2.color = 0

    
   # sleep(5)
    outcome = None
    while True:
        # sleep(0.1)
        # display.check_for_quit()
        # display.update(agent1.board.fen(), game_board)
        #print(agent1.material_balance(),agent1.mobility())
        if agent1.board.fullmove_number >= Player.MAX_MOVES:
           # print("EVALUATING WITH STOCKFISH ", end='')
            res = stockfish_eval(agent1.board)
            #print(res)
            return res

        assert agent1.board.fen() == agent2.board.fen()
        move = None
        if agent1.board.turn == agent1.color:
            move = agent1.select_move()
        else:
            move = agent2.select_move()

        agent1.board.push(move)
        agent2.board.push(move)
        if agent1.board.is_game_over():
            outcome = agent1.board.outcome()
            #display.update(agent1.board.fen(), game_board)
           # sleep(3)
            break
    res = outcome.winner
    if outcome.winner is None:
        res = 0.5
   # print(res)
    return res

def stockfish_eval(board):
    engine = chess.engine.SimpleEngine.popen_uci("/home/janek/dev/SI/prac4/chess/bosses/stockfish/stockfish-ubuntu-20.04-x86-64-avx2")
    info = engine.analyse(board, chess.engine.Limit(time=1))
    score = info['score'].white()
    engine.quit()
    if chess.engine.Cp(-100) <= score <= chess.engine.Cp(100):
        return 0.5
    if score > chess.engine.Cp(100):
        return 1
    return 0

if __name__ == '__main__':
    N = 80
    
    #game_board = display.start()
    agents = [random_agent() for _ in range(N)]
    results = [[0, 0] for _ in range(N)]

    for i in range(0, N):
        for j in range(i+1, N):
            print(f"AGENT {i}: ", end=' ')
            print(str(agents[i]))
            print(f"AGENT {j}: ", end=' ')
            print(str(agents[j]))
            res_1 = simulate(agents[i], agents[j])
            res_2 = simulate(agents[j], agents[i])
            if res_1 == 0.5 or res_2 == 0.5:
                results[i][0] += 1
                results[j][0] += 1

            results[i][1] += res_1 + (1- res_2)
            results[j][1] += res_2 + (1- res_1)
    
    final =  [(agent, res) for agent, res in zip(agents, results)]
    final.sort(key=cmp_to_key(lambda x1, x2 : x1[1][1] - x2[1][1]), reverse=True)

    with open('results.txt', 'a') as res:
        res.write('\n--------------------------------\n')
        res.write(f'{N} agents, {2*(N-1)} games each\n')
        for i in range(N):
            s = str(final[i][0]) + ' total: ' + str(final[i][1][1]) + f' with {final[i][1][0]} draws\n'
            print(s)
            res.write(s)

display.terminate()