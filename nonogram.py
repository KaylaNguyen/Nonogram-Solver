"""
CS 343 Final Project
# Nonogram Solver using Genetic Algorithm and Constraint Satisfaction
# Kayla Nguyen & Amna Aftab
"""
import random
from itertools import izip_longest


class Nonogram(object):
    # Define some character constants
    global BLANK, FILL, UNKNOWN, ROWS, COLUMNS, COLUMN_COUNT, ROW_COUNT, board
    BLANK = " "
    FILL = "#"
    UNKNOWN = "?"

    #### EXAMPLES

    # HEART (9x9)
    # ROWS = [[2, 2], [4, 4], [9], [9], [7], [5], [3], [1], [1]]
    # COLUMNS = [[3], [5], [6], [6], [7], [6], [6], [5], [3]]

    # ELEPHANT (15x15)
    # ROWS = [[3], [4, 2], [6, 6], [1, 4, 2, 1], [6, 3, 2], [6, 7], [6, 8], [1, 10], [1, 10], [1, 10], [1, 1, 4, 4], [3, 4, 4], [4, 4], [4, 4], [4, 4]]
    # COLUMNS = [[1], [10], [2, 3, 1], [6, 2], [6], [15], [1, 4, 8], [2, 9], [14], [8], [1, 6], [1, 10], [1, 10], [1, 11], [12]]

    # DUCK (15x15)
    ROWS = [[3], [5], [4, 3], [7], [5], [3], [5], [1, 8], [3, 3, 3], [7, 3, 2], [5, 4, 2], [8, 2], [10], [2, 3], [6]]
    COLUMNS = [[3], [4], [5], [4], [5], [6], [3, 2, 1], [2, 2, 5], [4, 2, 6], [8, 2, 3], [8, 2, 1, 1], [2, 6, 2, 1],
               [4, 6], [2, 4], [1]]

    # HOUSE (10x10)
    # ROWS = [[2, 1], [5], [6], [8], [10], [1, 1], [1, 2, 1, 1], [1, 2, 1, 1], [1, 2, 1], [8]]
    # COLUMNS = [[1], [7], [3, 1], [4, 4], [5, 4], [5, 1], [4, 2, 1], [5, 1], [7], [1]]

    # Weird random shape (15x15)
    # ROWS = [[2, 7, 2], [3, 4, 4], [3, 1, 5], [2, 1, 1, 3], [2, 1, 1, 2], [2, 1, 2], [2, 6], [5, 8], [4, 8], [11, 1, 1], [1, 8], [2, 1, 1, 5, 1], [1, 8, 3], [1, 5, 2], [1, 1, 2]]
    # COLUMNS = [[6, 1, 1, 4], [10, 1], [2, 5, 1], [3, 2], [1, 3, 1], [2, 5], [4, 4, 3], [2, 7], [5, 8], [1, 1, 9], [3, 1, 6], [3, 3, 2], [11, 1], [2, 6 ,3], [1, 4]]

    # weird random shape #2 (lamda)
    # ROWS = [[2], [1, 2], [1, 1], [2], [1], [3], [3], [2, 2], [2, 1], [2, 2, 1], [2, 3], [2, 2]]
    # COLUMNS = [[2, 1], [1, 3], [2, 4], [3, 4], [4], [3], [3], [3], [2], [2]]

    # Hen
    # ROWS = [[3],[2,1],[3,2],[2,2],[6],[1,5],[6],[1],[2]]
    # COLUMNS = [[1,2],[3,1],[1,5],[7,1],[5],[3],[4],[3]]


    ROW_COUNT = len(ROWS)
    COLUMN_COUNT = len(COLUMNS)
    # initialize board
    board = [[UNKNOWN for x in range(COLUMN_COUNT)] for y in range(ROW_COUNT)]


    # generate random solution for each constraint
    # returns a tuple in the form (row_solution, col_solution)
    def get_random_state(self, row_constraints, col_constraints):
        row_length = len(col_constraints)
        col_length = len(row_constraints)

        row_sol = []
        col_sol = []

        # solution based on row constraints
        for row in row_constraints:
            sol = self.get_permutations(row, row_length)  # get all possible permutations given a constraint
            row_sol.append(random.choice(sol))  # append a random permutation

        # solution based on column constraints
        for col in col_constraints:
            sol = self.get_permutations(col, col_length)  # get all possible permutations given a constraint
            col_sol.append(random.choice(sol))  # append a random permutation

        return row_sol, col_sol


    # gets all possible permutations in a row given the constraints
    # returns a list of all possible permutations
    def get_permutations(self, constraints, row_length):
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
            for p in self.get_permutations(constraints[1:], row_length - i - 1):
                prev = BLANK * (i - constraints[0])
                # add a blank space after placing a block
                perms.append(prev + blocks + BLANK + p)
        return perms


    # return a random row that meets the constraints
    def get_random_row(self, row_num):
        return random.choice(self.get_permutations(ROWS[row_num], ROW_COUNT))


    # check constrains for given row (board[row])
    def check_constraint_row(self, state, row):
        current_row = state[row]
        return self.check_constraint(ROWS, row, current_row)


    # check constrains for given column
    def check_constraint_col(self, state, column):
        current_col = []
        for x in range(0, ROW_COUNT):
            current_col.append(state[x][column])
        return self.check_constraint(COLUMNS, column, current_col)


    # return number of constraint violated, order matters
    # if there's more filled square in row than expected, each filled square is one violation
    # if there's more filled square in a sequence than expected, each extra filled square is a violation
    def check_constraint(self, constraints_list, index, current):
        violate = 0
        for constraint in constraints_list[index]:
            # flag to determine if the constraint is met
            flag = False
            for i in range(0, len(current)):
                if current[i] is FILL:
                    counter = 1
                    for j in range(i + 1, len(current)):
                        counter += 1
                        # print "checking " + str(j)
                        if current[j] is not FILL:
                            counter -= 1
                            break
                    if counter == constraint:
                        # print "Counter equals constrains"
                        # backtrack and remove that out of consideration
                        for a in range(0, constraint):
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


    def print_board(self):
        for r in board:
            print ' '.join(r)


    # Return true if there's no constraint violation in the solution
    def goal_check(self, solution):
        for i in range(0, ROW_COUNT):
            if self.check_constraint_row(solution, i) is not 0:
                return False
        for j in range(0, COLUMN_COUNT):
            if self.check_constraint_col(solution, j) is not 0:
                return False
        return True


    # Return true if there's no constraint violation in the solution
    def check_all_col(self, solution):
        num = 0
        for j in range(0, COLUMN_COUNT):
            num += self.check_constraint_col(solution, j)
        return num


    # list of rows/cols
    def print_state(self, state):
        string = ""
        for row in state:
            string += str(row)
            string += "\n"
        return string


    # orients each array vertically (like columns in the board)
    def row_to_col(self, game_board):
        col = []
        for x in izip_longest(*game_board, fillvalue=' '):
            col.append(''.join(x))
        return col


    def string_to_list(self, board):
        game = []
        for b in board:
            game.append(b.split())
        return game


    # getter methods
    def get_row_constraints(self):
        return ROWS


    def get_column_constraints(self):
        return COLUMNS


    def test(self):
        self.print_board()

        # check permutations
        for perm in self.get_permutations([2, 2], 7):
            print perm

        # check random state
        print "RANDOM STATE"
        state = self.get_random_state(ROWS, COLUMNS)

        col_sol = self.string_to_list(self.row_to_col(state[1]))
        print(self.print_state(state[0]))  # print solution generated based on row constraints only
        # check constraints each column
        counter = self.check_all_col(state[0])

        print "Number of col constraints violated: ", counter

        counter = 0
        print(self.print_state(self.row_to_col(state[1])))  # print solution generated based on column constraints only
        for row in range(0, ROW_COUNT):
            counter += self.check_constraint_row(col_sol, row)

        print "Number of row constraints violated: ", counter
        print "RANDOM ROW: ", self.get_random_row(0)


stuff = Nonogram()
# stuff.test()
