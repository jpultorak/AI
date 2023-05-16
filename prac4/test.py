import numpy as np
from copy import deepcopy
class A:
    
    def __init__(self, other = None) -> None:
        if other is None:
            self.default_constructor()
        else:
            self.copy_constructor(other)
    
    def default_constructor(self):
        self.A = np.array([1, 2, 3])
        self.x = 3

    def copy_constructor(self, other):
        self.A = np.copy(other.A)
        self.x = other.x

    def print(self):
        print(self.A, self.x)

    def change_fst(self):
        self.A[0] = -111
        self.x = 1666

# a1 = A()
# print(a1.A)
# a2 = A(a1)
# print(a2.A)
# a2.change_fst()
# a2.print()
# a1.print()

# a = np.array([1, 2, 3])
# b = np.array([3.6, -1, 8])
# print(np.dot(a, b))

