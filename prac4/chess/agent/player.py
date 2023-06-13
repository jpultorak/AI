import chess
import chess.polyglot
from os import environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
from chessboard import display
from functools import cmp_to_key
import sys
from time import sleep

class Player():
    DEPTH = 4
    QUIESENCE_DEPTH = 2
    # mobility factors
    KNIGHT_MOBILITY = 5.5
    BISHOP_MOBILITY = 4
    ROOK_MOBILITY = 1
    QUEEN_MOBILITY = 2
    KING_MOBILITY = 0

    PAWN_BLACK = [
        0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
        5,  5, 10, 25, 25, 10,  5,  5,
        0,  0,  0, 20, 20,  0,  0,  0,
        5, -5,-10,  0,  0,-10, -5,  5,
        5, 10, 10,-20,-20, 10, 10,  5,
        0,  0,  0,  0,  0,  0,  0,  0]

    PAWN_WHITE = [
        0,   0,   0,   0,   0,   0,   0,   0,
        5,   10,  10,  -20, -20, 10,  10,  5,
        5,   -5,  -10, 0,   0,   -10, -5,  5,
        0,   0,   0,   20,  20,  0,   0,   0,
        5,   5,   10,  25,  25,  10,  5,   5,
        10,  10,  20,  30,  30,  20,  10,  10,
        50,  50,  50,  50,  50,  50,  50,  50,
        0,   0,   0,   0,   0,   0,   0,   0]

    KNIGHT_BLACK = [
        -50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50]
    KNIGHT_WHITE = KNIGHT_BLACK

    BISHOP_BLACK = [
        -20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20]

    BISHOP_WHITE = [
        -20, -10, -10, -10, -10, -10, -10, -20,
        -10, 5, 0, 0, 0, 0, 5, -10,
        -10, 10, 10, 10, 10, 10, 10, -10,
        -10, 0, 10, 10, 10, 10, 0, -10,
        -10, 5, 5, 10, 10, 5, 5, -10,
        -10, 0, 5, 10, 10, 5, 0, -10,
        -10, 0, 0, 0, 0, 0, 0, -10,
        -20, -10, -10, -10, -10, -10, -10, -20]

    ROOK_BLACK = [
        0,  0,  0,  0,  0,  0,  0,  0,
        5, 10, 10, 10, 10, 10, 10,  5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
        0,  0,  0,  5,  5,  0,  0,  0]

    ROOK_WHITE = [
        0, 0, 0, 5, 5, 0, 0, 0,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        -5, 0, 0, 0, 0, 0, 0, -5,
        5, 10, 10, 10, 10, 10, 10, 5,
        0, 0, 0, 0, 0, 0, 0, 0]

    QUEEN_BLACK = [
        -20,-10,-10, -5, -5,-10,-10,-20,
        -10, 0,  0,  0,  0,  0,  0,-10,
        -10, 0,  5,  5,  5,  5,  0,-10,
        -5,  0,  5,  5,  5,  5,  0, -5,
         0,  0,  5,  5,  5,  5,  0, -5,
        -10, 5,  5,  5,  5,  5,  0,-10,
        -10, 0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20]

    QUEEN_WHITE = QUEEN_BLACK

    KING_MID_WHITE = [
        20, 40, 10, 0, 0, 10, 40, 20,
        20, 20, 0,  0,  0,   0,   20,  20,
        -10, -20, -20, -20, -20, -20, -20, -10,
        -20, -30, -30, -40, -40, -30, -30, -20,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30,
        -30, -40, -40, -50, -50, -40, -40, -30]

    KING_MID_BLACK = [
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
        20, 20,  0,  0,  0,  0, 20, 20,
        20, 30, 10,  0,  0, 10, 30, 20]

    KING_END = [
        -50, -30, -30, -30, -30, -30, -30, -50,
        -30, -30, 0,   0,   0,   0,   -30, -30,
        -30, -10, 20,  30,  30,  20,  -10, -30,
        -30, -10, 30,  40,  40,  30,  -10, -30,
        -30, -10, 30,  40,  40,  30,  -10, -30,
        -30, -10, 20,  30,  30,  20,  -10, -30,
        -30, -20, -10, 0,   0,   -10, -20, -30,
        -50, -40, -30, -20, -20, -30, -40, -50]

    MVV_LVA = [
    [15, 14, 13, 12, 11, 10], # victim P; attacker: P N B R Q K
    [25, 24, 23, 22, 21, 20], # victim N
    [35, 34, 33, 32, 31, 30], # victim B
    [45, 44, 43, 42, 41, 40], # victim R
    [55, 54, 53, 52, 51, 50], # victim Q
    [0, 0, 0, 0, 0, 0]        # victim K
    ]

    PST = [(PAWN_BLACK, PAWN_WHITE),
                     (KNIGHT_BLACK, KNIGHT_WHITE),
                     (BISHOP_BLACK, BISHOP_WHITE),
                     (ROOK_BLACK, ROOK_WHITE),
                     (QUEEN_BLACK, QUEEN_WHITE)]
    VAL = {
        chess.PAWN : 100,
        chess.BISHOP : 330,
        chess.KNIGHT : 320,
        chess.ROOK : 500,
        chess.QUEEN : 900,
        chess.KING : 0
    }
    def __init__(self, white=False):
        self.reset(white)

    def reset(self, white=False):
        self.board = chess.Board()
        self.color = white # 1 if white, 0 otherwise
        self.pieces_count = 14 # major (Q, R) and minor (N, B) pieces count
        self.eval = 0
        self.say('RDY')

    def get_attacked(self, piece, color):
        squares = self.board.pieces(piece_type=piece, color=color)
        attacked = chess.SquareSet()
        a = [self.board.attacks(sq) for sq in squares]
        for x in a:
            attacked.update(x)
        return attacked

    def mobility(self):
        res = 0
        w_pawns, b_pawns = self.get_attacked(chess.KNIGHT, True), self.get_attacked(chess.KNIGHT, False)
        w_knights, b_knights = self.get_attacked(chess.KNIGHT, True), self.get_attacked(chess.KNIGHT, False)
        w_bishops, b_bishops = self.get_attacked(chess.BISHOP, True), self.get_attacked(chess.BISHOP, False)
        w_rooks, b_rooks = self.get_attacked(chess.ROOK, True), self.get_attacked(chess.ROOK, False)
        w_queens, b_queens = self.get_attacked(chess.QUEEN, True), self.get_attacked(chess.QUEEN, False)

        # knights mobility
        res += Player.KNIGHT_MOBILITY*(len(w_knights.difference(b_pawns)) - len(b_knights.difference(w_pawns)))
        # bishops mobility
        res += Player.BISHOP_MOBILITY*(len(w_bishops.difference(b_pawns)) - len(b_bishops.difference(w_pawns)))
        # rooks mobility
        bad_w = b_pawns.union(b_bishops).union(b_knights)
        bad_b = w_pawns.union(w_bishops).union(w_knights)
        res += Player.ROOK_MOBILITY*(len(w_rooks.difference(bad_w)) - len(b_rooks.difference(bad_b)))

        # queens mobility
        bad_w = b_pawns.union(b_bishops).union(b_knights).union(b_rooks)
        bad_b = w_pawns.union(w_bishops).union(w_knights).union(w_rooks)
        res += Player.QUEEN_MOBILITY*(len(w_queens.difference(bad_w)) - len(b_queens.difference(bad_b)))

        return res

    def evaluate(self):
        return self.eval #+ self.mobility()

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

    def alpha_beta(self, alpha, beta, depth, max_player, capture):
        f = False
        if self.board.fullmove_number >= 40:
            f = True
        outcome = self.board.outcome(claim_draw=f)
        if outcome is not None: # game has ended
            res = outcome.winner
            if res is None:
                return 0, None
            if res:
                return float('inf'), None

            return float('-inf'), None

        if depth == 0:
            #if self.board.is_check() or capture:
             #   return self.quiescence_search(alpha, beta, Player.QUIESENCE_DEPTH, max_player)
            #print(self.board.unicode(),'\n',self.eval(),'\n', )
            return self.evaluate(), None


        
        moves = list(self.board.legal_moves)
        moves.sort(key=cmp_to_key(self.move_ordering), reverse=True)
        next_move =  moves[0]

        if max_player:
            value = float('-inf')
            for move in moves:
                x, y = self.eval, self.pieces_count
                capture = self.board.is_capture(move)
                self.do_move(move)
                
                child_value, unused_move = self.alpha_beta(alpha, beta, depth-1, False, capture)

                self.board.pop()
                self.eval, self.pieces_count = x, y # undo move

                if child_value > value:
                    value = child_value
                    next_move = move
                    alpha = max(value, alpha)

                if value >= beta:
                    break
        else:
            value = float('inf')
            for move in moves:
                x, y = self.eval, self.pieces_count
                capture = self.board.is_capture(move)
                self.do_move(move)  # do move

                child_value, unused_move = self.alpha_beta(alpha, beta, depth-1, True, capture)

                self.eval, self.pieces_count = x, y # undo move
                self.board.pop()

                if child_value < value:
                    value = child_value
                    next_move = move
                    beta = min(value, beta)

                if value <= alpha:
                    break

        return value, next_move
    
    def quiescence_search(self, alpha, beta, depth, max_player):
        outcome = self.board.outcome()
        if outcome is not None: # game has ended
            res = outcome.winner
            if res is None:
                return 0, None
            if res:
                return float('inf'), None

            return float('-inf'), None

        if depth == 0 :
            return self.evaluate(), None

        moves = [x for x in self.board.legal_moves if self.board.is_capture(x) or self.board.is_check()] 
        if not moves:
            return self.evaluate(), None
        
        moves.sort(key=cmp_to_key(self.move_ordering), reverse=True)
        next_move =  moves[0]

        if max_player:
            value = float('-inf')
            for move in moves:
                x, y = self.eval, self.pieces_count
                self.do_move(move)
                
                child_value, unused_move = self.quiescence_search(alpha, beta, depth-1, False)

                self.board.pop()
                self.eval, self.pieces_count = x, y # undo move

                if child_value > value:
                    value = child_value
                    next_move = move
                    alpha = max(value, alpha)

                if value >= beta:
                    break
        else:
            value = float('inf')
            for move in moves:
                x, y = self.eval, self.pieces_count
                self.do_move(move)  # do move

                child_value, unused_move = self.quiescence_search(alpha, beta, depth-1, True)

                self.eval, self.pieces_count = x, y # undo move
                self.board.pop()

                if child_value < value:
                    value = child_value
                    next_move = move
                    beta = min(value, beta)

                if value <= alpha:
                    break

        return value, next_move
    
    def is_endgame(self):
        return self.pieces_count <= 6

    def put_remove_piece(self, piece, square, remove):
        if piece.piece_type not in (chess.PAWN, chess.KING):
            if remove:
                self.pieces_count -= 1
            else:
                self.pieces_count += 1
        
        factor = 1
        if not piece.color:
            factor = -1
        if remove:
            factor *= -1

        self.eval += factor*Player.VAL[piece.piece_type]
        if piece.piece_type != chess.KING:
            self.eval += factor*Player.PST[piece.piece_type-1][piece.color][square]
            return

        if self.is_endgame():
            self.eval += factor*self.KING_END[square]
            return

        if piece.color:
            self.eval += factor*self.KING_MID_WHITE[square]
        else:
            self.eval += factor*self.KING_MID_BLACK[square]

    def do_move(self, move):
        
        sq_from, sq_to = move.from_square, move.to_square
        piece_from, piece_to = self.board.piece_at(sq_from), self.board.piece_at(sq_to)
        if piece_to is not None:  # remove taken piece
            self.put_remove_piece(piece_to, sq_to, remove=True)

        self.put_remove_piece(piece_from, sq_from, remove=True)
        if move.promotion is not None:
            self.put_remove_piece(chess.Piece(move.promotion, self.board.turn), sq_to, remove=False)
        else:
            self.put_remove_piece(piece_from, sq_to, remove=False)

        self.board.push(move)

    def select_move(self, max_time = 1000):  # max_time in ms
        _val, move = self.alpha_beta(float('-inf'), float('inf'), self.DEPTH, self.color, False)
        return move

    #---------------------Communication-------------------------#
    def say(self, what):
        sys.stdout.write(what)
        sys.stdout.write('\n')
        sys.stdout.flush()

    def hear(self):
        line = sys.stdin.readline().split()
        return line[0], line[1:]

    def loop(self):
        while True:
            # sleep(0.5)
            # display.check_for_quit()
            # display.update(self.board.fen(), game_board)
            cmd, args = self.hear()
            if cmd == 'HEDID':
                unused_move_timeout, unused_game_timeout = args[:2]
                move = args[2]
                self.do_move(chess.Move.from_uci(move))

            elif cmd == 'ONEMORE':
                #print("RESET", file=sys.stderr)
                self.reset()
                continue

            elif cmd == 'BYE':
                break
            else:
                assert cmd == 'UGO'
                #assert not self.game.move_list
               # print("WE ARE WHITE", file=sys.stderr)
                self.color = 1
            try:
                entry = reader.choice(agent.board)
                move = entry.move
            except IndexError:
                #print('No matching opening', file=sys.stderr)
                
                move = agent.select_move()

            #print(agent.board.fen(), file=sys.stderr)
            self.do_move(move)
            self.say('IDO ' + str(move))

if __name__ == '__main__':
   # game_board = display.start()
    with chess.polyglot.open_reader('/home/janek/dev/SI/prac4/chess/data/baron30.bin') as reader:
        agent = Player()
        agent.loop()
   