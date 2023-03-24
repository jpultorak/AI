from collections import deque
import heapq

class State:

    def __init__(self, K_pos, boxes, steps, prev, last_move) -> None:
        self.K_pos = K_pos
        self.boxes = boxes
        self.steps = steps
        self.prev = prev
        self.last = last_move

    def __hash__(self) -> int:
        return hash((self.K_pos, self.boxes))
    
    def __eq__(self, __o: object) -> bool:
        return self.K_pos == __o.K_pos and self.boxes == __o.boxes
    
    def __lt__(self, __o):
        return self.steps < __o.steps
    
    def __str__(self) -> str:
        return f'player pos: {self.K_pos}\nboxes:{list(self.boxes)}\nmoves from initial state:{self.steps}\nlast move: {self.last}'
    
class Board:
    # n -> rows count, m - cols count
    def __init__(self, n, m, board):
       
        self.n = n
        self.m = m
        self.board = board
        self.init_state, self.goals = self.clear_board()
        self.corners = self.precomp_corners()
    
    # save box and player position to state, in order to simplify board description
    # returns initial state
    def ending_state(self, state):
        return self.goals == state.boxes
    
    def dead_state(self, state):
        for box in state.boxes:
            if box in self.corners:
                return True
        return False
    
    def clear_board(self):
        player_pos = None
        boxes = []
        goals = []
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j] in ('+', 'K'):
                    player_pos = (i, j)
                elif self.board[i][j] in ('*', 'B'):
                    boxes.append((i, j))

                if self.board[i][j] in ('+', '*', 'G'):
                    goals.append((i, j))
                    self.board[i][j] = '.'
                elif self.board[i][j] in ('K', 'B'):
                    self.board[i][j] = '.'

        return State(player_pos, frozenset(boxes), 0, None, None), set(goals)

    def precomp_corners(self):
        def is_corner(x, y):
            if self.board[x][y] == 'W' or (x, y) in self.goals:
                return False 
            if self.board[x][y-1] == 'W' and (self.board[x-1][y] == 'W' or self.board[x+1][y] == 'W'):
                return True
            if self.board[x][y+1] == 'W' and (self.board[x-1][y] == 'W' or self.board[x+1][y] == 'W'):
                return True
            return False
        
        corners = []
        for i in range(1, self.n-1):
            for j in range(1, self.m-1):
                if is_corner(i, j):
                    corners.append((i, j))
        return set(corners)

    # goal: for each possible push, calculate needed distance
    # running bfs from given state
    def calc_dists(self, state):
        dist = [[-1 for _ in range(self.m)] for _ in range(self.n)]
        Q = deque()
        Q.append(state.K_pos)
        st_r, st_c = state.K_pos[0], state.K_pos[1]
        dist[st_r][st_c] = 0
        while Q:
            cur_r, cur_c = Q.popleft()
            for (dr, dc) in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                r, c = cur_r + dr, cur_c + dc
                # if considered cell is wall or a box, we cant move there
                if self.board[r][c] == 'W' or dist[r][c] != -1 or (r, c) in state.boxes:
                    continue

                dist[r][c] = dist[cur_r][cur_c] + 1
                Q.append((r, c))

        return dist
     
    def generate_states(self, state, cur_steps):
        dist = self.calc_dists(state)
        states = []
        for (r, c) in state.boxes:
            # push from left
            if dist[r][c-1] != -1 and (r, c+1) not in state.boxes and self.board[r][c+1] == '.':
                new_state = State((r, c), (state.boxes - frozenset([(r, c)])) | frozenset([(r, c+1)]), cur_steps + dist[r][c-1] + 1, state, 'R')
                states.append(new_state)

            # push from right
            if dist[r][c+1] != -1 and (r, c-1) not in state.boxes and self.board[r][c-1] == '.':
                new_state = State((r, c), (state.boxes - frozenset([(r, c)])) | frozenset([(r, c-1)]), cur_steps + dist[r][c+1] + 1, state, 'L')
                states.append(new_state)

            # push from below
            if dist[r+1][c] != -1 and (r-1, c) not in state.boxes and self.board[r-1][c] == '.':
                new_state = State((r, c), (state.boxes - frozenset([(r, c)])) | frozenset([(r-1, c)]), cur_steps + dist[r+1][c] + 1, state, 'U')
                states.append(new_state)

            # push from above
            if dist[r-1][c] != -1 and (r+1, c) not in state.boxes and self.board[r+1][c] == '.':
                new_state = State((r, c), (state.boxes - frozenset([(r, c)])) | frozenset([(r+1, c)]), cur_steps + dist[r-1][c] + 1, state, 'D')
                states.append(new_state)       

        return states

    def solve_bfs(self):
        # Q is min heap
        Q = []
        heapq.heappush(Q, self.init_state)
        visited = set([self.init_state])

        while Q:
            state = heapq.heappop(Q)
            visited.add(state)
            if self.ending_state(state):
                return state
            

            states = self.generate_states(state, state.steps)
            for next_state in states:
                if next_state in visited or self.dead_state(next_state):
                    continue
                
                heapq.heappush(Q, next_state)

    def prev_cell(self, cell, move):
        r, c = cell
        if move == 'R':
            c -= 1
        elif move == 'L':
            c += 1
        elif move == 'U':
            r += 1
        elif move == 'D':
            r -= 1
        return (r, c)
    
    # returns shortest path from current state to given cell
    def retrieve_path(self, state, cell):
        dist = [[-1 for _ in range(self.m)] for _ in range(self.n)]
        prev_move = [[None for _ in range(self.m)] for _ in range(self.n)]
        Q = deque()
        Q.append(state.K_pos)
        st_r, st_c = state.K_pos[0], state.K_pos[1]
        dist[st_r][st_c] = 0
        while Q:
            cur_r, cur_c = Q.popleft()
            for (dr, dc, move) in ((0, 1, 'R'), (0, -1, 'L'), (1, 0, 'D'), (-1, 0, 'U')):
                r, c = cur_r + dr, cur_c + dc
                # if considered cell is wall or a box, we cant move there
                if self.board[r][c] == 'W' or dist[r][c] != -1 or (r, c) in state.boxes:
                    continue

                dist[r][c] = dist[cur_r][cur_c] + 1
                prev_move[r][c] = move
                # found ending cell
                if (r, c) == cell:
                    path = []
                    while(prev_move[r][c] is not None):
                        path.append(prev_move[r][c])
                        (r, c) = self.prev_cell((r, c), prev_move[r][c])

                    return path
                Q.append((r, c))
        return []
    
    def solve(self):
        cur_state = game.solve_bfs()
        states = [cur_state]
        while(cur_state.prev is not None):
            cur_state = cur_state.prev
            states.append(cur_state)
        states.reverse()
        res = []
        for i in range(len(states)-1):
            
            dest = game.prev_cell(states[i+1].K_pos, states[i+1].last)
            path = game.retrieve_path(states[i], dest)
            path.reverse()
            path.append(states[i+1].last)
            res += path
        return res
    

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
        solution = ''.join(game.solve())
    
        out.write(solution)
       
