# CS 343 Final Project
# Nonogram Solver using Genetic Algorithm and Constraint Satisfaction
# Kayla Nguyen & Amna Aftab
import random 
import itertools 
from itertools import izip_longest
# Define some character constants
BLANK = "-"
FILL = "#"
UNKNOWN = "?"

# Constraints for rows and columns
ROWS = [[2, 2], [7], [2, 4], [7], [5], [3], [1]]

COLUMNS = [[3], [5], [2, 3], [6], [6], [5], [3]]

ROW_COUNT = len(ROWS)
COLUMN_COUNT = len(COLUMNS)
board = [[UNKNOWN for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]



# generate random solution for each constraint 
# returns a tuple in the form (row_solution, col_solution)
def get_random_state(row_constraints, col_constraints):
    row_length = len(col_constraints)
    col_length = len(row_constraints)

    row_sol = [] 
    col_sol = []

    # solution based on row constraints 
    for row in row_constraints:
        sol = get_permutations(row, row_length) # get all possible permutations given a constraint 
        row_sol.append(random.choice(sol)) # append a random permutation
    
    # solution based on column constraints
    for col in col_constraints:
        sol = get_permutations(col, col_length) # get all possible permutations given a constraint 
        col_sol.append(random.choice(sol)) # append a random permutation

    return row_sol, col_sol


# gets all possible permutations in a row given the constraints
# returns a list of all possible permutations 
def get_permutations(constraints, row_length):
    # create a block = size of the first constraint
    blocks = FILL * constraints[0]
    # base case: if 1 constraint
    if len(constraints) == 1:
        perms = []
        # place the block in every available location in row/col
        # move the block left -> right with each iteration
        for i in range(row_length - constraints[0] + 1):
            prev = BLANK * i  # spaces before block
            after = BLANK * (row_length - i - constraints[0])  # spaces after block
            perms.append(prev + blocks + after)
        return perms
    perms = []
    # iterate over all available empty spaces after the first block is placed
    for i in range(constraints[0], row_length):
        # recurse over remaining set of constraints
        for p in get_permutations(constraints[1:], row_length - i - 1):
            prev = BLANK * (i - constraints[0])
            # add a blank space after placing a block
            perms.append(prev + blocks + BLANK + p)
    return perms


# check constrains for given row (board[row])
# return number of constraint violated, order matters
# if there's more filled square in row than expected, each filled square is one violation
# if there's more filled square in a sequence than expected, each extra filled square is a violation
def check_constraint_row(row):
    print board[row]
    print ROWS[row]

    current_row = board[row]
    violate = 0
    # print current_row
    for constraint in ROWS[row]:
        # flag to determine if the constraint is met
        flag = False
        for i in range(0, len(current_row)):
            # print current_row
            # print "looking at index " + str(i)
            if current_row[i] is FILL:
                counter = 1
                for j in range(i + 1, len(current_row)):
                    counter += 1
                    # print "checking " + str(j)
                    if current_row[j] is not FILL:
                        counter -= 1
                        # print "current_row[i] is not fill at " + str(j)
                        # print "counter is " + str(counter)
                        break
                if counter == constraint:
                    # print "Counter equals constrains"
                    # backtrack and remove that out of consideration
                    for a in range(0, constraint):
                        # print "current row to delete is " + str(int(i+a))
                        current_row[i + a] = BLANK
                    # print current_row
                    flag = True
                    break
                else:
                    # print "Counter not equals constrains"
                    for a in range(0, counter):
                        # print "current row to delete is " + str(int(i + a))
                        current_row[i + a] = BLANK
                    # print current_row
                    break
        if flag is False:
            violate += 1

    # check for any addition fill blank
    for square in current_row:
        if square is FILL:
            # print 'square is filled'
            violate += 1

    print violate
    return violate

# TODO: make this not repetitive
# check constrains for given column
# return number of constraint violated, order matters
# if there's more filled square in row than expected, each filled square is one violation
# if there's more filled square in a sequence than expected, each extra filled square is a violation
def check_constraint_col(column):
    print COLUMNS[column]

    current_col = []
    for x in range(0, ROW_COUNT):
        current_col.append(board[x][column])

    print current_col

    violate = 0
    # print current_row
    for constraint in COLUMNS[column]:
        # flag to determine if the constraint is met
        flag = False
        for i in range(0, len(current_col)):
            # print current_row
            # print "looking at index " + str(i)
            if current_col[i] is FILL:
                counter = 1
                for j in range(i + 1, len(current_col)):
                    counter += 1
                    # print "checking " + str(j)
                    if current_col[j] is not FILL:
                        counter -= 1
                        # print "current_row[i] is not fill at " + str(j)
                        # print "counter is " + str(counter)
                        break
                if counter == constraint:
                    # print "Counter equals constrains"
                    # backtrack and remove that out of consideration
                    for a in range(0, constraint):
                        # print "current row to delete is " + str(int(i+a))
                        current_col[i + a] = BLANK
                    # print current_row
                    flag = True
                    break
                else:
                    # print "Counter not equals constrains"
                    for a in range(0, counter):
                        # print "current row to delete is " + str(int(i + a))
                        current_col[i + a] = BLANK
                    # print current_row
                    break
        if flag is False:
            violate += 1

    # check for any addition fill blank
    for square in current_col:
        if square is FILL:
            # print 'square is filled'
            violate += 1

    print violate
    return violate


def print_board():
    for r in board:
        print ' '.join(r)


# Return true if there's no constraint violation in the solution
def goal_check(solution):
    for row in solution:
        if check_constraint_row(row) is not 0:
            return False
    return True


# list of rows/cols
def print_state(board):
    for row in board: 
        print row 

# orients each array vertically (like columns in the board)
def row_to_col(board):
    col = [] 
    for x in izip_longest(*board, fillvalue=' '):
        col.append(''.join(x))
    return col


def main():
    print_board()
    # check constraint of row 2
    check_constraint_row(2)
    # check constraint of col 3
    check_constraint_col(3)

    # check permutations
    for perm in get_permutations([2, 2], 7):
        print perm

    # check random state 
    state = get_random_state(ROWS, COLUMNS)
    print_state(state[0]) # print solution generated based on row constraints only
    print_state(row_to_col(state[1])) # print solution generated based on column constraints only 


# run the main method
if __name__ == '__main__':
    main()