#!/usr/bin/env python3

import sys

def solve(readFile):
    # read the sudoku puzzle
    with open(readFile, 'r') as f:
        orig = f.readlines()

    # make a write file
    fileName = file[:file.find('.')]
    writeFile = f'{fileName}.out'

    # store the values in curr
    curr = [[0 for i in range(9)] for j in range(9)]
    for i in range(9):
        tmp = orig[i].split()
        for j in range(9):
            curr[i][j] = int(tmp[j])

    # possible values for a single spot
    jar = [[1 for i in range(9)] for j in range(81)]

    stepLimit = 20
    for step in range(stepLimit):
        for i in range(9):
            for j in range(9):
                celli = (i // 3) * 3
                cellj = (j // 3) * 3
                # enforce possibility depending on the possibilities
                # of other spots in rows, columns and cells
                if curr[i][j] == 0:
                    index = 0
                    oneCount = 0
                    setter = 0
                    for k in range(9):
                        if jar[i*9+j][k]:
                            index = k
                            oneCount += 1
                            # check all the rows, columns and cells
                            # to find if they have the same possibility
                            # row wise
                            others = 0
                            for x in range(9):
                                if x != j and jar[i*9+x][k]:
                                    others = 1
                                    break
                            if not others:
                                setter = 1
                                break
                            # column wise
                            others = 0
                            for y in range(9):
                                if y != i and jar[y*9+j][k]:
                                    others = 1
                                    break
                            if not others:
                                setter = 1
                                break
                            # cell wise
                            others = 0
                            for u in range(3):
                                for v in range(3):
                                    if cellj+v != j or celli+u != i:
                                        if jar[(celli+u)*9+cellj+v][k]:
                                            others = 1
                                            break
                            if not others:
                                setter = 1
                                break
                    # if only one possibility is nonzero
                    if oneCount < 2 or setter:
                        curr[i][j] = index + 1
                # deal with the consequences of a known value
                if curr[i][j]:
                    # self
                    jar[i*9+j] = [0 for _ in range(9)]
                    jar[i*9+j][curr[i][j]-1] = 1
                    # row wise
                    for x in range(9):
                        if x != j:
                            jar[i*9+x][curr[i][j]-1] = 0
                    # column wise
                    for y in range(9):
                        if y != i:
                            jar[y*9+j][curr[i][j]-1] = 0
                    # cell wise
                    for u in range(3):
                        for v in range(3):
                            if cellj+v != j and celli+u != i:
                                jar[(celli+u)*9+cellj+v][curr[i][j]-1] = 0

        # write into the output file
        with open(writeFile, 'a') as f:
            f.write(f'Iteration: {step+1}\n')
            for line in curr:
                f.write(str(line) + '\n')
            f.write('\n')

        # check if more iterations are needed
        hasZero = 0
        for line in curr:
            for entry in line:
                if entry == 0:
                    hasZero = 1
                    break
            if hasZero:
                break
        if not hasZero:
            print(f'Solved in {step+1} iterations.')
            return

    print(f'{stepLimit} iterations were executed without success. '
        + 'Sudoku is too hard for this program.')
    return

if __name__ == '__main__':
    files = sys.argv[1:]
    for file in files:
        solve(file)
