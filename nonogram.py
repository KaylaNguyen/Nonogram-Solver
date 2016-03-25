# CS 343 Final Project
# Nonogram Solver using Genetic Algorithm and Constraint Satisfaction
# Kayla Nguyen & Amna Aftab

# Define some character constants
BLANK = " "
FILL = "#"
UNKNOWN = "?"

# Constraints for rows and columns
ROWS = [[2, 2], [7], [2, 4], [7], [5], [3], [1]]

COLUMNS = [[3], [5], [2, 3], [6], [6], [5], [3]]

ROW_COUNT = len(ROWS)
COLUMN_COUNT = len(COLUMNS)
board = [[UNKNOWN for x in range(COLUMN_COUNT)] for x in range(ROW_COUNT)]


def get_permutations():
    return None


# check constrains for given row (board[row])
# return number of constraint violated
def check_constraint(row):
    # print board[row]
    print ROWS[row]

    # current_row = board[row]
    current_row = [FILL, FILL, UNKNOWN, FILL, FILL, FILL, UNKNOWN]
    counter = 0
    violate = 0
    print current_row
    for constraint in ROWS[row]:
        # flag to determine if the constraint is met
        flag = False
        for i in range(0, len(current_row)):
            if current_row[i] is FILL:
                counter += 1
                for j in range(i, len(current_row)):
                    if current_row[j] is not FILL:
                        print "current_row[i] is not fill at " + str(j)
                        break
            if counter == constraint:
                print "Counter equals constrains"
                # backtrack and remove that out of consideration
                for a in range(0, constraint):
                    current_row[i + a] = BLANK
                flag = True
                counter = 0
                break
        if flag is False:
            violate += 1
    print current_row

    print violate
    return violate


def print_board():
    for r in board:
        print ' '.join(r)


def goal_check():
    return None


def main():
    return None

main()
print_board()
check_constraint(0)
