import random
import numpy as np


class Nonogram:

    def __init__(self, no_rows, no_cols, rows, cols) -> None:
        self.no_rows = no_rows
        self.no_cols = no_cols
        self.rows = rows
        self.cols = cols
        # caching results from opt_dist
        self.cache = dict()

        # board initialization
        self.board =  None
        self.bad_rows = []
        self.reset()
        self.get_bad_rows()

        # maximum iterations when solving puzzle
        self.MAX_ITERATIONS = (self.no_rows + self.no_cols)*100

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
    
    def opt_dist(self, row, row_desc):
        row_tpl = tuple(row)
        #print(row, row_desc)
        if (row_tpl, row_desc) in self.cache:
            return self.cache[(row_tpl, row_desc)]
        
        n = len(row)
        k = len(row_desc)
        ones = [0 for _ in range(n+1)]
        for i in range(1, n+1):
            ones[i] = ones[i-1]
            if row[i-1] == 1:
                ones[i] += 1

        dp = [[1000 for _ in range(n+1)] for _ in range(k+2)]
        for j in range(1, n+1):
            dp[k+1][j] = ones[n] - ones[j-1]

        for i in range(k, 0, -1):
            block_len = row_desc[i-1]
            for j in range(1, n+1):
                for l in range(j, n-block_len+2):
                    r = l+block_len-1
        
                    n1 = block_len - (ones[r] - ones[l-1])
                    n2 = 0
                    if l != j:
                        n2 = ones[l-1] - ones[j-1]
                
                    n3 = 0 
                    if r+1 != n+1 and row[r] == 1:
                        n3 = 1

                    n4 = 1000
                    if i+1 == k+1 and r+2 > n:
                        n4 = 0
                    elif r+2 <= n:    
                        n4 = dp[i+1][r+2]

                    dp[i][j] = min(dp[i][j], n4 + n1 + n2 + n3)
        self.cache[(row_tpl, row_desc)] = dp[1][1]    
        return dp[1][1]
    
    def flip(self, px):
        return 1-px
    
    def check_solved(self):
        if self.bad_rows:
            return False
        for x, col in enumerate(self.board.T):
            if self.opt_dist(col, self.cols[x]) > 0:
                return False
        return True
    
    def get_bad_rows(self):
        bad_rows = []
        
        for x, row in enumerate(self.board):
            if self.opt_dist(row, self.rows[x]) > 0:
                bad_rows.append(x)
        
        self.bad_rows = bad_rows

    def reset(self):
        board = np.random.randint(0, 2, size=(self.no_rows, self.no_cols))
        self.board = board

    # how much flipping pixel improves board state
    def change_row(self, row_id, px):
        row_desc = self.rows[row_id]
        prev_val = self.opt_dist(self.board[row_id], row_desc)
        
        # flip pixel
        row_1 = np.copy(self.board[row_id])
        row_1[px] = self.flip(row_1[px])
        after_val = self.opt_dist(row_1, row_desc) 

        return prev_val- after_val
    
    def change_col(self, col_id, px):
        col_desc = self.cols[col_id]

        col = self.board[:, col_id]
        prev_val = self.opt_dist(col, col_desc)

        # flip pixel
        col_1 = np.copy(col)
        col_1[px] = self.flip(col_1[px])
        after_val = self.opt_dist(col_1, col_desc) 

        return prev_val- after_val
    
    # given a probability of an event, simulate wheter to do it or not
    def do_random_stfuff(self, probability):
        return np.random.uniform(0, 1) < probability
    
    def solve(self):
        for _ in range(self.MAX_ITERATIONS):

            if self.check_solved():
                return
            
            # if there are no bad rows 
            if not self.bad_rows or self.do_random_stfuff(0.2):
                row_id = np.random.randint(0, self.no_rows)
            else:
                row_id = random.choice(self.bad_rows)

            # at random choose random column
            if self.do_random_stfuff(0.2):
                col_id = np.random.randint(0, self.no_cols)
            else:
                # otherwise choosing best cell in that row
                res = [(self.change_col(col_id, row_id) + self.change_row(row_id, col_id), col_id) for col_id in range(0, self.no_cols)]
                col_id = max(res)[1]
            
            self.board[row_id][col_id] = self.flip(self.board[row_id][col_id])
            self.get_bad_rows()
        
        self.solve()

def read_row(s):
    s = s.strip()
    arr = s.split()
    arr = [int(x) for x in arr]
    return tuple(arr)

if __name__ == '__main__':
    with open('zad_input.txt', 'r') as inp, open('zad_output.txt', 'w') as out:
        s = inp.readline().split()
    
        no_rows, no_cols = int(s[0]), int(s[1])
        rows = [read_row(inp.readline()) for _ in range(no_rows)]
        cols = [read_row(inp.readline()) for _ in range(no_cols)]
        game = Nonogram(no_rows, no_cols, rows, cols)
  
        game.solve()
        out.write(str(game))
       