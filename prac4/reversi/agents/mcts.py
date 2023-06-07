import math
from collections import defaultdict

class MCTS:

    UCT_const = 1.414

    def __init__(self):
        self.U = defaultdict(int)   # total utility for a node
        self.N = defaultdict(int)   # n.o. playouts going through node
        self.tree = dict()   # for each node store its children

    def choose(self, node):
        def eval(node):
            return self.N[node]
        
        return max(self.tree[node], key=eval)
    
    def playout(self, node):
        
        path = self.selection(node)
        
        leaf = node.create_copy(path[-1])
        self.expand(leaf)
        result = self.simulate(leaf)
        assert result in [1, 0.5, 0]
        self.backpropagate(result, path)

    def selection(self, node):
        path = []
        while True:
            path.append(node)
            if node not in self.tree or not self.tree[node]:    # node is unexpanded or terminal
                return path
            node = self.uct_policy(node)
            
    def expand(self, node):   # add node to tree
        
        if node not in self.tree:
            self.tree[node] = node.generate_successors()

    def simulate(self, node):
        while True:
            if node.terminal():
                return node.utility()
            node = node.random_child()

    def backpropagate(self, result, path):

        if result == 0.5:
            for node in path:
                self.N[node] += 1
                self.U[node] += 0.5
            return
        
        for node in reversed(path):
            self.N[node] += 1
            if (node.player == 1 and result == 1) or (node.player == 0 and result == 0):
               self.U[node] += 1

    def uct_policy(self, node):

        logN_parent = math.log(self.N[node])
        def eval_uct(n):
            if self.N[n] == 0:   # unexplored node
                return math.inf
            return self.U[n]/self.N[n] + self.UCT_const * math.sqrt(logN_parent/self.N[n])
        
        return max(self.tree[node], key=eval_uct)
               

