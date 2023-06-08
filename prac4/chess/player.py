import chess
from chessboard import display

class Player():
    DEPTH = 5
    VAL = {
        chess.PAWN : 1,
        chess.BISHOP : 3,
        chess.KNIGHT : 3,
        chess.ROOK : 5,
        chess.QUEEN : 9,
        chess.KING : 0
    }
    def __init__(self, white=False):
        self.board = chess.Board()
        self.color = white # 1 if white, 0 otherwise

    def eval(self):
        res = 0
        for piece in [chess.PAWN, chess.BISHOP, chess.KNIGHT, chess.ROOK, chess.QUEEN, chess.KING]:
            res += Player.VAL[piece]*len(self.board.pieces(piece_type = piece, color=True))
            res = Player.VAL[piece]*len(self.board.pieces(piece_type = piece, color=True))

        return res
    
    def alpha_beta(self, alpha, beta, depth, max_player):
        outcome = self.board.outcome()
        if outcome is not None: # game has ended 
            res = outcome.winner
            if res is None:
                return 0, None
            if res:
                return float('inf'), None
            return float('-inf'), None

        if depth == 0:
            return self.eval(), None
        
        
        value, next_move = float('-inf'), None
        if not max_player:
            value = float('inf')

        if max_player:
            for move in self.board.legal_moves:
                self.board.push(move) # do move
                child_value, unused_move = self.alpha_beta(alpha, beta, depth-1, False) 
                self.board.pop() # undo move

                if child_value >= value:
                    value = child_value
                    next_move = move

                alpha = max(value, alpha)
                if value > beta:
                    break
        else:
            for move in self.board.legal_moves:
                self.board.push(move) # do move
                child_value, unused_move = self.alpha_beta(alpha, beta, depth-1, True) 
                self.board.pop() # undo move

                if child_value <= value:
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
    computer_white = False
    agent = Player(white=computer_white)
    print(agent.board)
    game_board = display.start()

    while True:
        display.check_for_quit()
        display.update(agent.board.fen(), game_board)

    display.terminate()
    while not agent.board.is_game_over():
        if agent.board.turn == agent.color:
            move = agent.do_move()
        else:
            move = input("Input move in uci format (e.g. e2e4): ")
            move = chess.Move.from_uci(move)
        agent.board.push(move)
        print(agent.board)