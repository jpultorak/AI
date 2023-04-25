import sys


def V(i,j):
    return 'V%d_%d' % (i,j)
    
def domains(Vs):
    return [ q + ' in 1..9' for q in Vs ]
    
def all_different(Qs):
    return 'all_distinct([' + ', '.join(Qs) + '])'
    
def get_column(j):
    return [V(i,j) for i in range(9)] 
            
def get_row(i):
    return [V(i,j) for j in range(9)] 
                        
def horizontal():   
    return [ all_different(get_row(i)) for i in range(9)]

def vertical():
    return [all_different(get_column(j)) for j in range(9)]

def block():
    res = []
    for i in range(0, 3):
        for j in range(0, 3):
                block = []
                for x in range(0, 3):
                        for y in range(0, 3):
                            block.append(V(x+i*3, y+j*3))
                res.append(all_different(block))
    return res

def print_constraints(Cs, indent, d):
    position = indent
    out.write (indent * ' ')
    out.write('\n')
    for c in Cs:
        out.write (c + ',')
        out.write ('\n')
        position += len(c)
        if position > d:
            position = indent
            out.write ('\n')
            out.write (indent * ' ')
            out.write ('\n')

def sudoku(assigments):
    variables = [ V(i,j) for i in range(9) for j in range(9)]
    
    out.write(':- use_module(library(clpfd)).\n')
    out.write ('solve([' + ', '.join(variables) + ']) :- \n')
    
    
    cs = domains(variables) + vertical() + horizontal() + block()
    for i,j,val in assigments:
        cs.append( '%s #= %d' % (V(i,j), val) )
    
    print_constraints(cs, 9, 70),
    out.write ('\n')
    out.write ('    labeling([ff], [' +  ', '.join(variables) + ']).\n' )
    out.write ('\n')
    out.write (':- solve(X), write(X), nl.\n')       

if __name__ == "__main__":
    raw = 0
    triples = []
    with open('zad_input.txt', 'r') as inp, open('zad_output.txt', 'w') as out:
        for x in inp:
            x = x.strip()
            if len(x) == 9:
                for i in range(9):
                    if x[i] != '.':
                        triples.append( (raw,i,int(x[i])) ) 
                raw += 1          
        sudoku(triples)
    
"""
89.356.1.
3...1.49.
....2985.
9.7.6432.
.........
.6389.1.4
.3298....
.78.4....
.5.637.48

53..7....
6..195...
.98....6.
8...6...3
4..8.3..1
7...2...6
.6....28.
...419..5
....8..79

3.......1
4..386...
.....1.4.
6.924..3.
..3......
......719
........6
2.7...3..
"""    
