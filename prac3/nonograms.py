import numpy as np


class Nonogram:

    def __init__(self, no_rows, no_cols, rows, cols) -> None:
        self.no_rows = no_rows
        self.no_cols = no_cols
        # row/col descriptions
        self.rows = rows
        self.cols = cols
        self.row_domain, self.col_domain = self.get_domains() 

        # board initialization
        self.board =  np.zeros((no_rows, no_cols))

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

    # given row/col description, generate its domain
    def gen_domain(self, desc, n):
        dom = []
        def f(cur_pos, block, res):

            if block == len(desc):
                dom.append(self.block_to_pixel(desc, res, n))
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
    
    # n = 5, desc = [2, 2], val = [0, 3] -> [1, 1, 0, 1, 1]
    def block_to_pixel(self, desc, val, n):
        res = [0]*n
        for block_len, block_pos in zip(desc, val):
            for i in range(block_pos, block_pos+block_len):
                res[i] = 1
        return res
    
    # given row/col, it's number and domain return two sets - pixels which must be on, and pixels
    # which must be off
    def intersect(self, domain):
        length = len(domain[0])

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

    def inference(self):
        # TODO
        pixels_on, pixels_off = set(), set()
        while not self.check_solved():
                
            for dom in self.row_domain:
                p1, p2 = self.intersect(dom)
                pixels_on |= p1
                pixels_off |= p2

            for dom in self.col_domain:
                p1, p2 = self.intersect(dom)
                pixels_on |= p1
                pixels_off |= p2
            
            for (x, y) in pixels_on:
                self.board[x, y] = 1

            self.constrain(pixels_on, pixels_off)
    # def check_solved(self):
    #     if self.bad_rows:
    #         return False
    #     for x, col in enumerate(self.board.T):
    #         if self.opt_dist(col, self.cols[x]) > 0:
    #             return False
    #     return True
    

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
  
        print(game.cols[0])
        print(game.col_domain[0])
        print(game.intersect(game.col_domain[0]))
       