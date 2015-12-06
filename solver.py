import pycosat
import sys
import string
import re
import string
#https://github.com/ContinuumIO/pycosat/blob/master/examples/sudoku.py helped out in creation
#only valid if the rows columns and blocks are correct
def grid_size(n):
    return n*n
def v(i, j, d,g_size):
    """
    Return the number of the variable of cell i, j and digit d,
    which is an integer in the range of 1 to 729 (including).
    """
    return grid_size(g_size) * (i - 1) + g_size * (j - 1) + d

def sudoku_clauses(n):
    res =[]
    for i in range(1, n+1):
        for j in range(1, n+1):
            res.append([v(i, j, d,n) for d in range(1, n+1)])
            for d in range(1, n+1):
                for dp in range(d + 1, n+1):
                    res.append([-v(i, j, d,n), -v(i, j, dp,n)])
    def valid(cells):
        for i, xi in enumerate(cells):
            for j, xj in enumerate(cells):
                if i < j:
                    for d in range(1, n+1):
                        res.append([-v(xi[0], xi[1], d,n), -v(xj[0], xj[1], d,n)])
    #checking the grids
    for i in range(1, n+1):
        valid([(i, j) for j in range(1, n+1)])
        valid([(j, i) for j in range(1, n+1)])
    # ensure 3x3 sub-grids "regions" have distinct values
    if n == 4:
        for i in 1, 3:
            for j in 1, 3:
                valid([(i + k % 2, j + k // 2) for k in range(n)])
    elif n == 9:
        for i in 1, 4, 7:
            for j in 1, 4 ,7:
                valid([(i + k % 3, j + k // 3) for k in range(n)])
    elif n == 25:
        for i in 1, 6, 11, 16 ,21:
            for j in 1, 6, 11, 16 ,21:
                valid([(i + k % 5, j + k // 5) for k in range(n)])
    else:
        print "not valid"
    return res

def solve(grid,n):

    clauses = sudoku_clauses(n)
    for i in range(1, n+1):
        for j in range(1, n+1):
            d = grid[i - 1][j - 1]
            if d:
                clauses.append([v(i, j, d,n)])

    # solve the SAT problem need to add the import
    sol = set(pycosat.solve(clauses))

    def read_cell(i, j):
        # return the digit of cell i, j according to the solution
        for d in range(1, n+1):
            if v(i, j, d,n) in sol:
                return d

    for i in range(1, n+1):
        for j in range(1, n+1):
            grid[i - 1][j - 1] = read_cell(i, j)

def parser(file):
    f = open(file, 'r')
    lines = f.readlines()
    f.close()
    matrix_res = []
    for line in lines:
        line = line.replace('\n','')
        line = line.replace(' ','')
        row = []
        for c in line:

            if c == '.':
                row.append(0)
            elif ord(c) >= 65:
                row.append(ord(c)-55)
            else:
                row.append(int(c))
        matrix_res.append(row)
    return matrix_res

def doc_write(solution):
    output = open("result.txt",'a')

    for line in solution:
        s = ''
        for n in line:
            if n >= 10:
                s += chr(n+55) +','
            else:
                s += str(n) +','
        s = s[:-1]
        output.write(s + '\n')

if __name__ == '__main__':
    from pprint import pprint
    hard = parser('challenge1.txt')
    # pprint(hard)
    solve(hard,4)
    # pprint(hard)
    doc_write(hard)
