import random
import numpy as np
from z4 import opt_dist

class Nonogram:

    def __init__(self, no_rows, no_cols, rows, cols) -> None:
        self.no_rows = no_rows
        self.no_cols = no_cols
        self.rows = rows
        self.cols = cols

        # board initialization
        self.board =  None
        self.bad_rows = []
        self.reset()
        self.get_bad_rows()
        # maximum iterations when solving puzzle
        self.MAX_ITERATIONS = 500

    def __repr__(self) -> str:
        res = ''
        for row in self.board:
            for el in row:
                if el:
                    res += '#'
                else: 
                    res += '.'
            res += '\n'
        return res[:-1]

    def flip(self, px):
        return 1-px
    
    def check_solved(self):
        if self.bad_rows:
            return False
        for x, col in enumerate(self.board.T):
            if opt_dist(col, self.cols[x]) > 0:
                return False
        return True
    
    def get_bad_rows(self):
        bad_rows = []
        
        for x, row in enumerate(self.board):
            if opt_dist(row, self.rows[x]) > 0:
                bad_rows.append(x)
        
        self.bad_rows = bad_rows

    def reset(self):
        board = np.random.randint(0, 2, size=(self.no_rows, self.no_cols))
        self.board = board

    # how much flipping pixel improves board state
    def change_row(self, row_id, px):
        block_length = self.rows[row_id]
        prev_val = opt_dist(self.board[row_id], block_length)
        
        # flip pixel
        row_1 = np.copy(self.board[row_id])
        row_1[row_id] = self.flip(row_1[row_id])
        after_val = opt_dist(row_1, block_length) 

        return prev_val- after_val
    
    def change_col(self, col_id, px):
        block_length = self.cols[col_id]

        col = self.board[:, col_id]
        prev_val = opt_dist(col, block_length)

        # flip pixel
        col_1 = np.copy(col)
        col_1[px] = self.flip(col_1[px])
        after_val = opt_dist(col_1, block_length) 

        return prev_val- after_val
    
    # given a probability of an event, simulate wheter to do it or not
    def do_random_stfuff(self, probability):
        return np.random.uniform(0, 1) < probability
    
    def solve(self):
        for _ in range(self.MAX_ITERATIONS):

            if self.check_solved():
                return
            
            # if there are no bad rows 
            if not self.bad_rows or self.do_random_stfuff(0.1):
                row_id = np.random.randint(0, self.no_rows)
            else:
                row_id = random.choice(self.bad_rows)

            # at random choose random column
            if self.do_random_stfuff(0.05):
                col_id = np.random.randint(0, self.no_cols)
            else:
                # otherwise choosing best cell in that row
                res = [(self.change_col(col_id, row_id) + self.change_row(row_id, col_id), col_id) for col_id in range(0, self.no_cols)]
                col_id = max(res)[1]
            
            self.board[row_id][col_id] = self.flip(self.board[row_id][col_id])
            self.get_bad_rows()
        
        self.solve()


if __name__ == '__main__':
    with open('zad5_input.txt', 'r') as inp, open('zad5_output.txt', 'w') as out:
        s = inp.readline()
        no_rows, no_cols = int(s[0]), int(s[2:])
        rows = [int(inp.readline()) for _ in range(no_rows)]
        cols = [int(inp.readline()) for _ in range(no_cols)]
        # print(no_rows, no_cols)
        # print(rows)
        # print(cols)
        test = Nonogram(no_rows, no_cols, rows, cols)
        #print(test)
        test.solve()
        out.write(str(test))
        #print(test)