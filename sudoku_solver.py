import numpy as np
import time
import os

# just defining a few global variables to use
# maybe later versions might have different size sudokus
check = True
SIZE = 9
# Do you want to analyze the real runtime of this program?
check_time = True

# -1's should be specified for unfilled locations 
# in our input file 
def read_input(file):
    matrix = []
    for i in range(SIZE):
        row = map(int, file.readline().split())
        matrix.append(row)
    return matrix 

def print_matrix(matrix):
    j = 0
    for k in range(SIZE+2):
        new_row = ''
        for i in range(SIZE):
            if i == 3 or i == 6:
                new_row += ' | ' + str(matrix[j][i])
            elif k == 3 or k == 7:
                new_row += '-' * 22
                j -= 1
                break
            else: 
                new_row += ' ' + str(matrix[j][i])
        print new_row
        j += 1

# this should just simply make sure that the rules of sudoku are satisfied 
# 1. Each row must have numbers 1 - 9
# 2. Each column must have numbers 1 - 9
# 3. Each square must have number 1 - 9
def check_input(matrix):
    # check rows 
    for j in range(SIZE):
        num_check = [False] * 9

        for i in range(0, SIZE):
            if matrix[j][i] > 9 or matrix[j][i] < 1 or num_check[matrix[j][i] - 1] == True:
                return False
            else:
                num_check[matrix[j][i]-1] = True
    # check columns
    for i in range(SIZE):
        num_check = [False] * 9
        for j in range(0, SIZE):
            if matrix[j][i] > 9 or matrix[j][i] < 1 or num_check[matrix[j][i] - 1] == True:
                return False
            else:
                num_check[matrix[j][i]-1] = True
    # check blocks
    for block in range(SIZE):
        num_check = [False] * 9
        # j is our row i is our col
        for j in range(SIZE/3):
            for i in range(SIZE/3):
                colIdx = (i + block*3) % SIZE
                rowIdx = (j + block/3 * 3)
                if matrix[rowIdx][colIdx] > 9  or matrix[rowIdx][colIdx] < 1 or num_check[matrix[rowIdx][colIdx] - 1] == True:
                    return False
                else:
                    num_check[matrix[rowIdx][colIdx] - 1] = True
    return True


# given an index into the matrix, what are possible values? 
def get_possible_values(matrix, i, j):
    if matrix[j][i] != -1 and matrix[j][i] != 0:
        return matrix[j][i]
    else:
        # ok so we know we haven't filled this value in
        # so then let's find all the possible values that this cell could be
        possible_values = set(range(1,10))
        col_values = set()
        row_values = set()
        for k in range(SIZE):
            row_values.add(matrix[j][k])
        for k in range(SIZE):
            col_values.add(matrix[k][i])    
        # it would be ideal if we coudl get the numbers in the block
        row_set = set(row_values)
        col_set = set(col_values)
        block_set = get_block_values(matrix, i, j)
        possible_values = possible_values.difference(row_set)
        possible_values = possible_values.difference(col_set)
        possible_values = possible_values.difference(block_set)
        possible_values = list(possible_values)
        return possible_values

def get_block(matrix, col, row):
    set_to_return = set()
    for i in range(col-3, col):
        for j in range(row-3, row):
            set_to_return.add(matrix[j][i])
    return set_to_return
     
def get_block_values(matrix, i, j):
    if i < 3 and j < 3: 
        return get_block(matrix, 3, 3)
    elif i < 6 and j < 3:
        # second block
        return get_block(matrix, 6, 3)
    elif i < 9 and j < 3:
        # third block
        return get_block(matrix, 9, 3)
    elif i < 3 and j < 6:
        # fourth block
        return get_block(matrix, 3, 6)
    elif i < 6 and j < 6:
        # fifth block
        return get_block(matrix, 6, 6)
    elif i < 9 and j < 6:
        # sixth block
        return get_block(matrix, 9, 6)
    elif i < 3 and j < 9:
        # 7th block
        return get_block(matrix, 3, 9)
    elif i < 6 and j < 9:
        # 8th block
        return get_block(matrix, 6, 9)
    elif i < 9 and j < 9:
        # 9th block
        return get_block(matrix, 9, 9)
    else:
        #error
        raise ValueError 
    
def get_unfilled_cell(matrix, i, j):
    # k is like the column or i
    # l is like the row or j
    for k in range(0, 9):
        for l in range(0, 9):
            if matrix[l][k] < 1:
                return (k,l)
    return (-1, -1) 

# ok so let's think about a sudoku board
# maybe we could use some type of dynamic programming solution? 
# like consider this number being here. what does that mean for other squares?
# we also have to consider if the square is already filled  
def solve_sudoku(matrix):
    copy_matrix = matrix
    ans = SS_help(copy_matrix, 0, 0)
    if ans[0]:
        return ans[1]
    return None

# lets pick a number for being in a square and then recurisvely try to fill it in
RECURSION_DEPTH = 0
def SS_help(matrix, i, j):
    global RECURSION_DEPTH 
    RECURSION_DEPTH += 1
    if check_input(matrix):
        # we have solved our sudoku 
        return (True, matrix)
    else:
        # ok so our matrix is not good
        unfilled_col, unfilled_row = get_unfilled_cell(matrix,i,j)
        if (unfilled_col, unfilled_row) == (-1, -1) and check_input(matrix):
            return (True, matrix)
        if (unfilled_col, unfilled_row) == (-1, -1) and not check_input(matrix):
            return (False, matrix)
        poss_val = get_possible_values(matrix, unfilled_col, unfilled_row)
        if len(poss_val) == 0:
            # this means there are not any possible solutions and the matrix is 
            # shitty. We need to backtrack
            matrix[unfilled_row][unfilled_col] = 0 #-1
            return (False, matrix)
        elif len(poss_val) == 1:
            # this means there is only one possible solution for our given spot 
            matrix[unfilled_row][unfilled_col] = poss_val[0]
            ans = SS_help(matrix, unfilled_col, unfilled_row)
            if ans[0]:
                return (True, matrix)
            else:
                matrix[unfilled_row][unfilled_col] = 0 #-1
                return (False, matrix)
        else:
            # there are multiple possible solutions 
            # we need to try them one at a time and if our sudoku is perfect short out
            for val in poss_val:
                matrix[unfilled_row][unfilled_col] = val
                ans = SS_help(matrix, unfilled_col, unfilled_row)
                if ans[0]:
                    return (True, matrix)
            # if this line is not here, then we are not backtracking 
            # the program will literally not work without this
            # which should make sense
            matrix[unfilled_row][unfilled_col] = 0 #-1
            return (False, matrix)
                    
                
def print_solved_board(solved):
    if solved == None:
        print("There is no solution. :(")
    else:
        print("The solution is the following sudoku:")
        print_matrix(solved)

if __name__ == '__main__':
    while True:
        print ' '
        print '-'*24 
        print '     SUDOKU SOLVER!'
        print '-'*24 
        print 'Menu:'
        print '-----'
        print '0: Use a file with a sudoku'
        print '1: Use stdin for a sudoku'
        print '2: Default entry'
        print '3: Cycle through input_directory'
        print 'q: Exit the solver'
        decision = raw_input("Please enter a menu command: ")
        if decision == '0':
            filename = raw_input("Please enter the filename: ")
            f = open(filename)
            matrix = read_input(f)
            print_matrix(matrix)

            if check:
                valid = check_input(matrix)
                print("Our sudoku board is appropriate. {}".format(valid))

            print("Please wait... solving the sudoku now")
            solved_board = solve_sudoku(matrix)
            print_solved_board(solved_board)
            f.close()

        elif decision == '1':
            print("Please enter your board as a matrix. Hit enter for each row of the sudoku. -1 indicates open position. ")
            matrix = []
            for _ in range(9):
                row = map(int, raw_input().split())
                matrix.append(row)
            print_matrix(matrix)
            solved_board = solve_sudoku(matrix)
            print_solved_board(solved_board)

        elif decision == '2':
            f = open('default.txt')
            matrix = read_input(f)
            print_matrix(matrix)
            solved = solve_sudoku(matrix)
            print_solved_board(solved)

        elif decision == '3':
            directory = 'solve_puzzles/'
            solution_dict = {}
            for filename in os.listdir(directory):
                if filename[0:6] == 'sudoku' and len(filename) == 14:
                    f = open(directory+filename)
                    matrix = read_input(f)
                    if check_time:
                        t0 = time.time()
                    print("Attempting to solve sudoku from filename: {}".format(filename))
                    solved = solve_sudoku(matrix)
                    if solved == None:
                        print "There is no solution"
                    else: 
                        print("Solved sudoku with filename: {}".format(filename))
                        if check_time:
                            t1 = time.time()
                            print("Time to solve sudoku: {}".format(t1-t0))
                        solution_dict[filename[7:10]] = solved
            for filename in os.listdir(directory):
                if filename[0:6] == 'sudoku' and len(filename) == 23:
                    f = open(directory+filename)
                    matrix = read_input(f)
                    print("Comparing answer from filename: {}".format(filename))
                    if solution_dict[filename[7:10]] == matrix:
                        print "The solution is correct"
                    else: 
                        print "Error with solver."

        elif decision == 'q':
            print 'Quitting the solver...'
            break
        else: 
            print 'That was not a valid command. Please try again.'

