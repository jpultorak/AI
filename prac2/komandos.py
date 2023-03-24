from collections import deque
import random

class State:
    # dir -> move used to reach this state
    def __init__(self, start, prev, dir, depth = None) -> None:
        self.start = start
        self.prev = prev
        self.dir = dir
        self.depth = depth
        # evaluation function, needed for a star algorithm
        self.f = None

    def __len__(self):
        return len(self.start)
    
    def __hash__(self) -> int:
        return hash(self.start)
    
    def __eq__(self, __o: object) -> bool:
        return self.start == __o.start
    
    def __lt__(self, __o: object) -> bool:
        return self.f < __o.f
    
class Board:
    
    def __init__(self, n, m, board) -> None:
        self.n = n
        self.m = m
        self.board = board
        self.init_state, self.goals = self.clear_board()

    def clear_board(self):
        goals, start = [], []
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] == 'G':
                    goals.append((i, j))
                    self.board[i][j] = ' '
                elif self.board[i][j] == 'S':
                    start.append((i, j))
                    self.board[i][j] = ' '
                elif self.board[i][j] == 'B':
                    goals.append((i, j))
                    start.append((i, j))
                    self.board[i][j] = ' '

        return  State(frozenset(start), None, None, 0), frozenset(goals)
    
    def end_state(self, state):
        for st in state.start:
            if st not in self.goals:
                return False
        return True
    
    # dir -> 'R' 'L' 'U' 'D'
    def move_dir(self, cell, dir):
        r, c = cell
        if dir == 'R':
            c += 1
        elif dir == 'L':
            c -= 1
        elif dir == 'U':
            r -= 1
        elif dir == 'D':
            r += 1
        # if new coord is a wall, we dont move
        if self.board[r][c] == '#':
            return cell
        return (r, c)
    
    def move_state(self, state, dir):
        new_start = []
        for st in state.start:
            new_start.append(self.move_dir(st, dir))
        
        return State(frozenset(new_start), state, dir, state.depth + 1)
    
    def reduce_uncertainty(self, upper):
        while True:
            states = [self.move_state(self.init_state, dir) for dir in ('L', 'R', 'U', 'D')]
            mi = min([len(st) for st in states])
            mi_states = [st for st in states if len(st) == mi]
            state = random.choice(mi_states)
            self.init_state = state
            if mi <= upper:
                break

    # change initial state by random moves
    def random_moves(self, total):
        for _ in range(total):
            dir = random.choice(('R', 'L', 'U', 'D'))
            #print(f'random move: {dir}!\n')
            self.init_state = self.move_state(self.init_state, dir)
    
    # starting form state, retrieve path
    def retrieve_path(self, state):
        res = []
        while state.prev is not None:
            res.append(state.dir)
            state = state.prev
        res.reverse()
        return ''.join(res)
    
    def bfs(self):
        Q = deque()
        visited = set()
        Q.appendleft(self.init_state)
        visited.add(self.init_state)

        best = len(self.init_state)
        while Q:
            state = Q.pop()
            if len(state) > best:
                continue
            
            for dir in ('L', 'R', 'U', 'D'):
                new_state = self.move_state(state, dir)
                if new_state in visited:
                    continue
                if self.end_state(new_state):
                    return self.retrieve_path(new_state)
                
                best = len(new_state)
                Q.appendleft(new_state)
                visited.add(new_state)
        return ''

    def print_state(self, state):
        for r in range(self.n):
            for c in range(self.m):
                if (r, c) in self.goals and (r, c) in state.start:
                    print('B', end='')
                elif (r, c) in self.goals:
                    print('G', end='')
                elif (r, c) in state.start:
                    print('S', end='')
                elif self.board[r][c] == '#':
                    print('#', end='')
                else:
                    print(' ', end='')
            print()

if __name__ == '__main__':
   
    board = []
    with open('zad_input.txt', 'r') as inp, open('zad_output.txt', 'w') as out:
        for line in inp.readlines(): 
            row = []
            for r in line:
                if(r != '\n'):
                    row.append(r)
            board.append(row)

        m = len(board[0])
        n = len(board)

        game = Board(n, m, board)
        #game.reduce_uncertainty(7)
        res = game.bfs()
        print(len(res))

        out.write(res)