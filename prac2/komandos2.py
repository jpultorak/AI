from komandos import Board, State
from collections import deque
import heapq

class Komandos(Board):
    def __init__(self, n, m, board) -> None:
        super().__init__(n, m, board)
        self.dist = self.precomp_dists()

    def heuristic(self, state, admissible = True):
        if not admissible:
            # W -> non-admissibility indicator; W = 0 -> BFS
            W = 0.65
            state.f = state.depth + W*sum([self.dist[st_r][st_c] for st_r, st_c in state.start])
        else:
            state.f = state.depth + max([self.dist[st_r][st_c] for st_r, st_c in state.start]) 

    def precomp_dists(self):
        dists = [[-1 for _ in range(self.m)] for _ in range(self.n)]
        Q =  deque()
        for r in range(self.n):
            for c in range(self.m):
                if (r, c) in self.goals:
                    dists[r][c] = 0
                    Q.append((r, c))
        while Q:
            cur_r, cur_c = Q.pop()
            for dr, dc in ((0, 1), (0, -1), (1, 0), (-1, 0)):
                r, c = cur_r + dr, cur_c + dc
                if self.board[r][c] == '#' or dists[r][c] != -1:
                    continue
                dists[r][c] = dists[cur_r][cur_c] + 1
                Q.appendleft((r, c))

        return dists

    def astar(self, admissible = True):
        Q = [self.init_state]
        visited = set()

        while Q:
            state = heapq.heappop(Q)
            visited.add(state)
            if self.end_state(state):
                return self.retrieve_path(state)
            
            for dir in ('L', 'R', 'U', 'D'):
                new_state = self.move_state(state, dir)
                if new_state in visited:
                    continue
                self.heuristic(new_state, admissible)
                heapq.heappush(Q, new_state)


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

        game = Komandos(n, m, board)
        res = game.astar(admissible=False)
        print(len(res))
    
        out.write(res)
                
                
