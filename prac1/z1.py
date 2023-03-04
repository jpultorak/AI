from collections import deque

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']

def valid_coords(xy, n = 8):
    if xy[0] < 1 or xy[0] > n or xy[1] < 1 or xy[1] > n:
        return False 
    return True 

# checks if xy1 is between xy2 and xy3
def check_between(xy1, xy2, xy3):
    if xy1[0] == xy2[0] == xy3[0]:
        mi = min(xy2[1], xy3[1])
        mx = max(xy2[1], xy3[1])
        return mi <= xy1[1] <= mx
    
    if xy1[1] == xy2[1] == xy3[1]:
        mi = min(xy2[0], xy3[0])
        mx = max(xy2[0], xy3[0])
        return mi <= xy1[0] <= mx
    
    return False
# val < 64
def int_to_coords(val):
    x = val // 8 + 1
    y = val % 8 + 1
    return (x, y)

def coord_to_int(xy):
    return 8*(xy[0]-1) + xy[1] - 1

def coord_to_chess(xy):
    return f'{letters[xy[0]-1]}{xy[1]}'

def chess_to_coords(pos):
    x = ord(pos[0]) - ord('a') + 1
    y = int(pos[1])
    return (x, y)

class Board_state:

    def __init__(self, white_move, bking_xy, wking_xy, rook_xy) -> None:
        self.white_move = white_move
        self.bking_xy = bking_xy
        self.wking_xy = wking_xy
        self.rook_xy = rook_xy

        self.check = self.is_attacked()

    def __str__(self) -> str:
        if self.white_move:
            player = 'white'
        else:
            player = 'black'

        if self.rook_xy is None:
            return f'(W) K{coord_to_chess(self.wking_xy)}\n(B) K{coord_to_chess(self.bking_xy)}\n({player} to move)'
        
        return f'(W) K{coord_to_chess(self.wking_xy)} R{coord_to_chess(self.rook_xy)}\n(B) K{coord_to_chess(self.bking_xy)}\n({player} to move)\n'
    
    def is_attacked(self):
        if self.rook_xy is None:
            return False
        
        if self.bking_xy[0] == self.rook_xy[0]:
            mx = max(self.bking_xy[1], self.rook_xy[1])
            mi = min(self.bking_xy[1], self.rook_xy[1])

            if self.wking_xy[0] == self.bking_xy[0] and self.wking_xy[1] < mx and self.wking_xy[1] > mi:
                return False
            return True
        
        if self.bking_xy[1] == self.rook_xy[1]:
            mx = max(self.bking_xy[0], self.rook_xy[0])
            mi = min(self.bking_xy[0], self.rook_xy[0])

            if self.wking_xy[1] == self.bking_xy[1] and self.wking_xy[0] < mx and self.wking_xy[0] > mi:
                return False
            return True
        
    def is_valid(self):
        bking_x, bking_y = self.bking_xy
        wking_x, wking_y = self.wking_xy

        if abs(bking_x - wking_x)**2 + abs(bking_y - wking_y)**2 <= 2:
            return False
        
        if self.rook_xy is None:
            return True
        
        if self.bking_xy == self.wking_xy or self.bking_xy == self.rook_xy or self.rook_xy == self.wking_xy:
            return False
        
        # if rook is taken from the board then valid
        if self.rook_xy is None:
            return True   
        # if black is checked and white is to move return false
        if self.check and self.white_move:
            return False 
        
        return True

    # return all possible states after moving king
    def king_move(self):
        res = []

        if self.white_move:
            king_x, king_y = self.wking_xy
        else: 
            king_x, king_y = self.bking_xy
    
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy and dx == 0:
                    continue
                
                newx = king_x + dx
                newy = king_y + dy
                if not valid_coords((newx, newy)):
                    continue
                
                if self.white_move:
                    new_state = Board_state(not self.white_move, self.bking_xy, (newx, newy), self.rook_xy)
                else:
                    new_state = Board_state(not self.white_move, (newx, newy), self.wking_xy, self.rook_xy)
                if new_state.is_valid():
                    res.append(new_state)
    
        return res

    # return all possible states moving rook
    def rook_move(self):
        if not self.white_move:
            return []
        
        res = []
        rook_x, rook_y = self.rook_xy
        
        x_cords = (i for i in (1, 8) if i != rook_x)
        y_cords = (i for i in (1, 8) if i != rook_y)

    
        for newx in x_cords:
            new_rook_xy = (newx, rook_y)
            if valid_coords(new_rook_xy) and not check_between(self.wking_xy, new_rook_xy, self.rook_xy) and not check_between(self.bking_xy, new_rook_xy, self.rook_xy):
                new_state = Board_state(not self.white_move, self.bking_xy, self.wking_xy, new_rook_xy)
                if new_state.is_valid():
                    res.append(new_state)

        for newy in y_cords:
            new_rook_xy = (rook_x, newy)
            if valid_coords(new_rook_xy) and not check_between(self.wking_xy, new_rook_xy, self.rook_xy) and not check_between(self.bking_xy, new_rook_xy, self.rook_xy):
                new_state = Board_state(not self.white_move, self.bking_xy, self.wking_xy, new_rook_xy)
                if new_state.is_valid():
                    res.append(new_state)  
        return res
    
    def check_mate(self):
        if not self.check or self.white_move:
            return False
        rook_safey = abs(self.rook_xy[1] - self.bking_xy[1]) >= 2
        rook_safex = abs(self.rook_xy[0] - self.bking_xy[0]) >= 2

        if self.bking_xy[0] == 1 and self.wking_xy[0] == 3 and self.wking_xy[1] == self.bking_xy[1] and rook_safey:
            return True

        if self.bking_xy[0] == 8 and self.wking_xy[0] == 6 and self.wking_xy[1] == self.bking_xy[1] and rook_safey:
            return True
        
        if self.bking_xy[1] == 1 and self.wking_xy[1] == 3 and self.wking_xy[0] == self.bking_xy[0] and rook_safex:
            return True

        if self.bking_xy[1] == 8 and self.wking_xy[1] == 6 and self.wking_xy[0] == self.bking_xy[0] and rook_safex:
            return True
        
        bking_corner = False
        if self.bking_xy == (1, 1) or self.bking_xy == (1, 8) or self.bking_xy == (8, 1) or self.bking_xy == (8, 8):
            bking_corner = True

        if not bking_corner:
            return False
        

        if abs(self.wking_xy[0] - self.bking_xy[0]) == 1 and abs(self.wking_xy[1] - self.bking_xy[1]) == 2 and abs(rook_xy[1] - self.wking_xy[1]) == 2:
            return True
        if abs(self.wking_xy[0] - self.bking_xy[0]) == 2 and abs(self.wking_xy[1] - self.bking_xy[1]) == 1 and abs(rook_xy[0] - self.wking_xy[0]) == 2:
            return True
       
        return False

    

def get_state_index(state):
    return (state.white_move, coord_to_int(state.bking_xy), coord_to_int(state.wking_xy), coord_to_int(state.rook_xy))

# depth -> maximum ammount of moves
def BFS(white_move,  start_bkingxy, start_wkingxy, start_rookxy):
    res = [[[[(None, None) for _ in range(0, 64)] for _ in range(0, 64)] for _ in range(0, 64)] for _ in range(2)]
    
    S = deque()
    # first state has distance 0
    res[white_move][coord_to_int(start_bkingxy)][coord_to_int(start_wkingxy)][coord_to_int(start_rookxy)] = (0, None)
    S.append(Board_state(white_move, start_bkingxy, start_wkingxy, start_rookxy))

    while S:
        state = S.popleft()

        # reached earliest mate
        if state.check_mate():
            return (state, res)

        dist = res[state.white_move][coord_to_int(state.bking_xy)][coord_to_int(state.wking_xy)][coord_to_int(state.rook_xy)][0]
        for new_state in state.king_move():

            id = get_state_index(new_state)
            if res[id[0]][id[1]][id[2]][id[3]][0] is not None:
                continue
    
            # moving king
            if state.white_move:
                move = ('K', state.wking_xy)
            else:
                move = ('K', state.bking_xy)

            res[id[0]][id[1]][id[2]][id[3]] = (dist+1, move)
            S.append(new_state)

        for new_state in state.rook_move():
            id = get_state_index(new_state)
        
            if res[id[0]][id[1]][id[2]][id[3]][0] is not None:
                continue
        
            # moving rook to next state
            move = ('R', state.rook_xy)
            res[id[0]][id[1]][id[2]][id[3]] = (dist+1, move)
            S.append(new_state)

    

if __name__ == '__main__':
    s = input().split()
    if s[0] == 'white':
        white_moves = True
    else: 
        white_moves = False

    wking_xy = chess_to_coords(s[1])
    rook_xy = chess_to_coords(s[2])
    bking_xy = chess_to_coords(s[3])
    end_state, dp = BFS(white_moves, bking_xy, wking_xy, rook_xy)
    white_moves ,bking_xy, wking_xy, rook_xy = (end_state.white_move, end_state.bking_xy, end_state.wking_xy, end_state.rook_xy)

    res = []
    while(dp[white_moves][coord_to_int(bking_xy)][coord_to_int(wking_xy)][coord_to_int(rook_xy)][0] != 0): 
        move = dp[white_moves][coord_to_int(bking_xy)][coord_to_int(wking_xy)][coord_to_int(rook_xy)][1]
        if move[0] == 'R':
            full_move = coord_to_chess(move[1]) + coord_to_chess(rook_xy)
            rook_xy = move[1]
        elif white_moves:
            full_move =  coord_to_chess(move[1])+ coord_to_chess(bking_xy)
            bking_xy = move[1]
        else:
            full_move = coord_to_chess(move[1]) + coord_to_chess(wking_xy)
            wking_xy = move[1]
    
        white_moves = not white_moves 
        res.append(full_move)
    
    print(' '.join(reversed(res)))