import chess
import chess.polyglot
import chess.gaviota

board = chess.Board()

w_knights = board.pieces(piece_type=chess.KNIGHT, color=True)
for q in sq
print(w_knights)

# mv = chess.Move.from_uci('e2e4')
# board.push(mv)
# with chess.polyglot.open_reader('baron30.bin') as reader:
#     for entry in reader.find_all(board):
#         print(entry.move, entry.weight)
#     print(reader.choice(board))
# BISHOP_BLACK = [-20,-10,-10,-10,-10,-10,-10,-20,
#             -10,  0,  0,  0,  0,  0,  0,-10,
#             -10,  0,  5, 10, 10,  5,  0,-10,
#             -10,  5,  5, 10, 10,  5,  5,-10,
#             -10,  0, 10, 10, 10, 10,  0,-10,
#             -10, 10, 10, 10, 10, 10, 10,-10,
#             -10,  5,  0,  0,  0,  0,  5,-10,
#             -20,-10,-10,-10,-10,-10,-10,-20]

# matrix = np.array(BISHOP_BLACK)
# m2 = np.reshape(matrix, (8, 8))
# #print(np.transpose(a))

# #print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in m2]))
# print('\n'.join([', '.join([str(cell) for cell in row]) for row in np.flipud(m2)]))