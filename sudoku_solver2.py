from pysat.solvers import Glucose3

def print_sudoku_grid(model):
    rows = [[] for _ in range(9)]

    for variable in model:
        if variable > 0:
            rows[int(str(variable)[0])-1].append(str(variable)[2])
    
    for row in rows:
        print(''.join(row))
    
variables = []

for i in range(1000):
    if len(str(i)) == 3 and str(i)[1] != '0' and str(i)[2] != '0':
        variables.append(True)
    else:
        variables.append(False)

sudoku_grid = []

for m in range(9):
    row = str(input())
    for n in range(9):
        if row[n] != '-':
            for v in range(1, 10):
                if v != int(row[n]):
                    variables[(m+1)*100+(n+1)*10+v] = False

clauses = []

for m in range(1, 10):
    for n in range(1, 10):
        clause = []
        for v in range(1, 10):
            clause.append(m*100+n*10+v)
        clauses.append(clause)

for v in range(1, 10):
    for m in range(1, 10):
        for n0 in range(1, 9):
            for n1 in range(n0+1, 10):
                clauses.append([-(100*m+10*n0+v), -(100*m+10*n1+v)])

for v in range(1, 10):
    for n in range(1, 10):
        for m0 in range(1, 9):
            for m1 in range(m0+1, 10):
                clauses.append([-(100*m0+10*n+v), -(100*m1+10*n+v)])

for m in range(1, 10):
    for n in range(1, 10):
        for w in range(1, 10):
            for v in range(1, 10):
                if v != w:
                    clauses.append([-(m*100+n*10+w), -(m*100+n*10+v)])

for m in range(1, 3):
    for n in range(1, 3):
        for v in range(1, 9):
            for x0 in (3*m-2, 3*m-1, 3*m):
                for x1 in (3*m-2, 3*m-1, 3*m):
                    for y0 in (3*n-2, 3*n-1, 3*n):
                        for y1 in (3*n-2, 3*n-1, 3*n):
                            if (x0, y0) < (x1, y1):
                                clauses.append([-(x0*100+y0*10+v), -(x1*100+y1*10+v)])

for i in range(1, 1000):
    if (variables[i] == False):
        clauses.append([-i])

while 1:
    with Glucose3(bootstrap_with=clauses) as solver:
        is_solvable = solver.solve()
        if not is_solvable:
            break
        
        model = solver.get_model()
        print_sudoku_grid(model)
        clauses.append([-x for x in model])

    