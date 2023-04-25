def B(i,j):
    return 'B_%d_%d' % (i,j)

def domains(Vs):
    return [ q + ' in 0..1' for q in Vs ]

def rowsum(total, i, C):
    return ' + '.join([B(i, j) for j in range(C)]) + f' #= {total}'

def colsum(total, j, R):
    return ' + '.join([B(i, j) for i in range(R)]) + f' #= {total}'

def sums(cols, rows, C, R):
    return [rowsum(rows[i], i, C) for i in range(R)] + [colsum(cols[i], i, R) for i in range(C)]

def all_triples(triples):
    return [f'{B(tr[0], tr[1])} #= {tr[2]}' for tr in triples]

def square(i, j):
    a, b, c, d = B(i, j), B(i, j+1), B(i+1, j), B(i+1, j+1)
    return f'{a} + {b} + {c} + {d} #= 1 #\/ {a} + {d} #= {b}+{c}'

def squares(C, R):
    return [square(i, j) for i in range(R-1) for j in range(C-1)]

def rowTriple(i, j):
    return f'{B(i, j+1)} #==> {B(i, j)} + {B(i, j+2)} #>0'

def colTriple(i, j):
    return f'{B(i+1, j)} #==> {B(i, j)} + {B(i+2, j)} #>0'

def col_rowTriples(C, R):
    return [rowTriple(i, j) for i in range(R) for j in range(C-2)] + [colTriple(i, j) for i in range(R-2) for j in range(C)]

def storms(rows, cols, triples):
    output.write(':- use_module(library(clpfd)).\n')
    
    R = len(rows)
    C = len(cols)
    
    bs = [ B(i,j) for i in range(R) for j in range(C)]
    
    output.write('solve([' + ', '.join(bs) + ']) :- \n')
    cs = domains(bs) + sums(cols, rows, C, R) + all_triples(triples)  + col_rowTriples(C, R) + squares(C, R)
    #cs = domains(bs) + col_rowTriples(C, R)
    for x in cs:
        writeln(x)

    output.write('    labeling([ff], [' +  ', '.join(bs) + ']).\n' )
    output.write('\n')
    output.write(":- solve(X), write(X), nl, told.\n") 

def writeln(s):
    output.write(s + ',\n')

txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(tuple(map(int, txt[i].split())))

storms(rows, cols, triples)            
        

