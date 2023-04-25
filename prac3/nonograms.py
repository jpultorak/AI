import numpy as np
import copy


class Nonogram:

    def __init__(self, no_rows, no_cols, rows, cols) -> None:
        self.no_rows = no_rows
        self.no_cols = no_cols
        # row/col descriptions
        self.rows = rows
        self.cols = cols
        # domains -> sets
        self.row_domain, self.col_domain = self.get_domains() 

        # board initialization
        self.board =  np.zeros((no_rows, no_cols))

    def __repr__(self) -> str:
        res = ''
        for row in self.board:
            for el in row:
                if el == 1:
                    res += '#'
                elif el == -1: 
                    res += '.'
                elif el == 0:
                    res += '?'
            res += '\n'
        return res[:-1]
    
    # n = 5, desc = [2, 2], val = [0, 3] -> [1, 1, 0, 1, 1]
    def block_to_pixel(self, desc, val, n):
        res = [0]*n
        for block_len, block_pos in zip(desc, val):
            for i in range(block_pos, block_pos+block_len):
                res[i] = 1
        return tuple(res)
    
    # given row/col description, generate its domain
    def gen_domain(self, desc, n):
        dom = set()
        def f(cur_pos, block, res):

            if block == len(desc):
                dom.add(self.block_to_pixel(desc, res, n))
                return
            
            while cur_pos <= n - desc[block]:
                # place the block
                temp = res + (cur_pos, )
                f(cur_pos + desc[block] + 1, block+1, temp)
                cur_pos += 1
        f(0, 0, ())
        return dom

    def get_domains(self):
        return [self.gen_domain(row, self.no_cols) for row in self.rows], [self.gen_domain(col, self.no_rows) for col in self.cols]
    
    def flip(self, px):
        return 1-px  
    
    # given row/col, it's number and domain return two sets - pixels which must be on, and pixels
    # which must be off
    def intersect(self, domain, length):
        res = [-2]*length
        for val in domain:
            for i in range(0, length):
                if res[i] == -2:
                    res[i] = val[i]

                elif res[i] == -1:
                    continue

                elif val[i] != res[i]:
                    res[i] = -1         
        return res
    # constrain domain of rows/cols given known pixels
    def constrain(self, px_on, px_off):

        constrained = False
        for i, j in px_on:
            bad = set()
            for val in self.row_domain[i]:
                if val[j] == 0:
                    bad.add(val)
                    constrained = True
            self.row_domain[i] -= bad

            bad.clear()
            for val in self.col_domain[j]:
                if val[i] == 0:
                    bad.add(val)
                    constrained = True
            self.col_domain[j] -= bad

        for i, j in px_off:
            bad = set()
            for val in self.row_domain[i]:
                if val[j] == 1:
                    bad.add(val)
                    constrained = True
            self.row_domain[i] -= bad

            bad.clear()
            for val in self.col_domain[j]:
                if val[i] == 1:
                    bad.add(val)
                    constrained = True

            self.col_domain[j] -= bad

        return constrained
    
    def inference(self):
        pixels_on, pixels_off = set(), set()
        while True:
                
            for i, dom in enumerate(self.row_domain):
                int = self.intersect(dom, self.no_cols)
                for j in range(self.no_cols):
                    if int[j] == 1:
                        pixels_on.add((i, j))
                        self.board[i, j] = 1
                    elif int[j] == 0:
                        pixels_off.add((i, j))
                        self.board[i, j] = -1

            for i, dom in enumerate(self.col_domain):
                int = self.intersect(dom, self.no_rows)
                for j in range(self.no_rows):
                    if int[j] == 1:
                        pixels_on.add((j, i))
                        self.board[j, i] = 1
                    elif int[j] == 0:
                        pixels_off.add((j, i))
                        self.board[j, i] = -1

            # if unable to constrain further, break the loop
            if not self.constrain(pixels_on, pixels_off):
                break
        
        # if domain becomes empty, it means its impossible to solve the puzzle
        for dom in self.row_domain:
            if not dom:
                return False
        
        for dom in self.col_domain:
            if not dom:
                return False
        # return changed pixels (needed to backtrack later)
        return pixels_on, pixels_off
    

    def backtrack(self, row_id):
        if row_id == self.no_rows:
            return True
        
        for val in self.row_domain[row_id]:
            
            prev_col, prev_row, prev_board = copy.deepcopy(self.col_domain), copy.deepcopy(self.row_domain), copy.deepcopy(self.board)
            #print("BEFPRE: ", prev_board)
            # make an assigment
            self.row_domain[row_id] = {val}
            result = self.inference()
            if result != False:
                result = self.backtrack(row_id+1)
                if result:
                    return True
                
            self.row_domain = prev_row
            self.col_domain = prev_col
            self.board = prev_board
           # print("after: ", prev_board)

        return False
        # select row/column
    

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
        #print(game)
        game.backtrack(0)
        #game.inference()
        out.write(str(game))
        # print(game.cols[4])
        # print(game.col_domain[4])
        # print(game.intersect(game.row_domain[0], 5))
        # game.constrain({(0, 0)}, {})
        # print(game.row_domain[0])