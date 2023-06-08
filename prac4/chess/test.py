import chess


board = chess.Board()

for mv in board.legal_moves:
    print(mv.from_square)
