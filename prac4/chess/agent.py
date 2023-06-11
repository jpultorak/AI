import chess
import chess.polyglot
from time import sleep
from chessboard import display

class Player():
    DEPTH = 4
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
        0,      0,      0,      0,      0,      0,      0,      0,
        5,      10,     10,     -20,    -20,    10,     10,     5,
        5,      -5,     -10,    0,      0,      -10,    -5,     5,
        0,      0,      0,      20,     20,     0,      0,      0,
        5,      5,      10,     25,     25,     10,     5,      5,
        10,     10,     20,     30,     30,     20,     10,     10,
        50,     50,     50,     50,     50,     50,     50,     50,
        0,      0,      0,      0,      0,      0,      0,      0]
    
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

    KING_MID_WHITE = [20,     30,     10,     0,      0,      10,     30,     20,
                20,     20,     0,      0,      0,      0,      20,     20,
                -10,    -20,    -20,    -20,    -20,    -20,    -20,    -10,
                -20,    -30,    -30,    -40,    -40,    -30,    -30,    -20,
                -30,    -40,    -40,    -50,    -50,    -40,    -40,    -30,
                -30,    -40,    -40,    -50,    -50,    -40,    -40,    -30,
                -30,    -40,    -40,    -50,    -50,    -40,    -40,    -30,
                -30,    -40,    -40,    -50,    -50,    -40,    -40,    -30]
    
    KING_MID_BLACK = [-30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -30,-40,-40,-50,-50,-40,-40,-30,
                -20,-30,-30,-40,-40,-30,-30,-20,
                -10,-20,-20,-20,-20,-20,-20,-10,
                20, 20,  0,  0,  0,  0, 20, 20,
                20, 30, 10,  0,  0, 10, 30, 20]
    
    KING_END = [-50,    -30,    -30,    -30,    -30,    -30,    -30,    -50,
                -30,    -30,    0,      0,      0,      0,      -30,    -30,
                -30,    -10,    20,     30,     30,     20,     -10,    -30,
                -30,    -10,    30,     40,     40,     30,     -10,    -30,
                -30,    -10,    30,     40,     40,     30,     -10,    -30,
                -30,    -10,    20,     30,     30,     20,     -10,    -30,
                -30,    -20,    -10,    0,      0,      -10,    -20,    -30,
                -50,    -40,    -30,    -20,    -20,    -30,    -40,    -50]
    
    PIECES_TABLES = [(PAWN_BLACK, PAWN_WHITE), 
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
        self.board = chess.Board()
        self.color = white # 1 if white, 0 otherwise

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

    #def king_safety(self):

    def eval(self):
        res = 0
        for piece in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN]:
            white_squares = self.board.pieces(piece_type = piece, color=True)
            black_squares = self.board.pieces(piece_type = piece, color=False)
            res += Player.VAL[piece]*len(white_squares)
            res -= Player.VAL[piece]*len(black_squares)

            for square in white_squares:
                res += Player.PIECES_TABLES[piece-1][1][square]

            for square in black_squares:
                res -= Player.PIECES_TABLES[piece-1][0][square]
        
        white_king, black_king = self.board.king(color=True), self.board.king(color=False)

        queens = (self.board.pieces(piece_type=chess.QUEEN, color=True), self.board.pieces(piece_type=chess.QUEEN, color=False))  # simple endgame condition - no queens
        if any(queens):
           res += Player.KING_MID_WHITE[white_king]
           res -= Player.KING_MID_BLACK[black_king]
        else:
            res += Player.KING_END[white_king]
            res -= Player.KING_END[black_king]

        return res + self.mobility()
    
    def alpha_beta(self, alpha, beta, depth, max_player):
        outcome = self.board.outcome()
        if outcome is not None: # game has ended 
            res = outcome.winner
            if res is None:
                return 0, None
            if res:
                return float('inf'), None
            return float('-inf'), None

        if depth == 0 :
            #print(self.board.unicode(),'\n',self.eval(),'\n', )
            return self.eval(), None
      
        
        next_move =  None
        if max_player:
            value = float('-inf')
            for move in self.board.legal_moves:
            
                self.board.push(move) # do move
                # if depth == 1 and (self.board.is_check()): # if the situation is dynamic, increase the depth
                #     depth = 2
                child_value, unused_move = self.alpha_beta(alpha, beta, depth-1, False) 
                self.board.pop() # undo move

                if child_value > value:
                    value = child_value
                    next_move = move
                    alpha = max(value, alpha)
                
                if value >= beta:
                    break
        else:
            value = float('inf')
            for move in self.board.legal_moves:
                self.board.push(move) # do move
                # if depth == 1 and (self.board.is_check()): # if the situation is dynamic, increase the depth
                #     depth = 2
                child_value, unused_move = self.alpha_beta(alpha, beta, depth-1, True) 
                self.board.pop() # undo move

                if child_value < value:
                    value = child_value
                    next_move = move
                    beta = min(value, beta)

                if value <= alpha:
                    break
            
        return value, next_move
    
    def do_move(self):
        _val, move = self.alpha_beta(float('-inf'), float('inf'), Player.DEPTH, self.color)
        return move

if __name__ == '__main__':
    computer_white = True
    agent = Player(white=computer_white)

    game_board = display.start()
    
    with chess.polyglot.open_reader('baron30.bin') as reader:
        while True:

            print(agent.eval(), agent.board.fen())
            display.check_for_quit()
            display.update(agent.board.fen(), game_board)

            if agent.board.turn == agent.color:
                try:
                    entry = reader.choice(agent.board)
                    move = entry.move
                except IndexError:
                    print("No matching opening!")
                    move = agent.do_move()
            else:
                move = None
                while not agent.board.is_legal(move):
                    move = input("Input move in uci format (e.g. e2e4): ")
                    try:
                        move = chess.Move.from_uci(move)
                    except:
                        move = None
                        print("Not a legal move!")
        
            agent.board.push(move)
            if agent.board.is_game_over():
                display.update(agent.board.fen(), game_board)
                sleep(3)
                break
display.terminate()