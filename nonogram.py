# CS 343 Final Project
# Nonogram Solver using Genetic Algorithm and Constraint Satisfaction
# Kayla Nguyen & Amna Aftab
import random
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
# initialize board
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
        sol = get_permutations(row, row_length)  # get all possible permutations given a constraint
        row_sol.append(random.choice(sol))  # append a random permutation
    
    # solution based on column constraints
    for col in col_constraints:
        sol = get_permutations(col, col_length)  # get all possible permutations given a constraint
        col_sol.append(random.choice(sol))  # append a random permutation

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
def check_constraint_row(state, row):
    # print board[row]
    # print ROWS[row]

    current_row = state[row]
    return check_constraint(ROWS, row, current_row)


# check constrains for given column
def check_constraint_col(state, column):
    # print COLUMNS[column]

    current_col = []
    for x in range(0, ROW_COUNT):
        current_col.append(state[x][column])
    #
    # print "current col"
    # print current_col

    return check_constraint(COLUMNS, column, current_col)


# return number of constraint violated, order matters
# if there's more filled square in row than expected, each filled square is one violation
# if there's more filled square in a sequence than expected, each extra filled square is a violation
def check_constraint(constraints_list, index, current):
    violate = 0
    for constraint in constraints_list[index]:
        # flag to determine if the constraint is met
        flag = False
        for i in range(0, len(current)):
            # print current_row
            # print "looking at index " + str(i)
            if current[i] is FILL:
                counter = 1
                for j in range(i + 1, len(current)):
                    counter += 1
                    # print "checking " + str(j)
                    if current[j] is not FILL:
                        counter -= 1
                        # print "current_row[i] is not fill at " + str(j)
                        # print "counter is " + str(counter)
                        break
                if counter == constraint:
                    # print "Counter equals constrains"
                    # backtrack and remove that out of consideration
                    for a in range(0, constraint):
                        # print "current row to delete is " + str(int(i+a))
                        current[i + a] = BLANK
                    # print current_row
                    flag = True
                    break
                else:
                    # print "Counter not equals constrains"
                    for a in range(0, counter):
                        # print "current row to delete is " + str(int(i + a))
                        current[i + a] = BLANK
                    # print current_row
                    break
        if flag is False:
            violate += 1

    # check for any addition fill blank
    for square in current:
        if square is FILL:
            # print 'square is filled'
            violate += 1

    # print violate
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
def print_state(state):
    for row in state:
        print row 


# orients each array vertically (like columns in the board)
def row_to_col(game_board):
    col = [] 
    for x in izip_longest(*game_board, fillvalue=' '):
        col.append(''.join(x))
    return col

def string_to_list(board):
    game = [] 
    for b in board:
        game.append(b.split())
    return game 


def main():
    print_board()
    # check constraint of row 2
    # check_constraint_row(board, 2)
    # check constraint of col 3
    # check_constraint_col(board, 3)

    # check permutations
    for perm in get_permutations([2, 2], 7):
        print perm

    # check random state
    print "RANDOM STATE"
    state = get_random_state(ROWS, COLUMNS)
   # row_sol = string_to_list(state[0])
    col_sol = string_to_list(row_to_col(state[1]))
    #print_state(state[0])  # print solution generated based on row constraints only
    #print_state(state[1])
    counter = 0
    # check constraints each column
    for col in range(0, COLUMN_COUNT):
        counter += check_constraint_col(state[0], col)

    print "Number of col constraints violated: ", counter

    counter = 0
    # TODO row_to_col doesn't return a 2D array?
    # print_state(row_to_col(state[1]))  # print solution generated based on column constraints only
    # NOTE: I'm not sure why check_constraint_row handles input differently from 
    # check constraint column. But they seem to require entirely different inputs to do the same job. ??? 
    for row in range(0, ROW_COUNT):
        counter+= check_constraint_row(col_sol, row)

    print "Number of row constraints violated: ", counter


# run the main method
if __name__ == '__main__':
    main()
