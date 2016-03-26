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
# return number of constraint violated, order matters
# if there's more filled square in row than expected, each filled square is one violation
# if there's more filled square in a sequence than expected, each extra filled square is a violation
def check_constraint(row):
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
                for j in range(i+1, len(current_row)):
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


def print_board():
    for r in board:
        print ' '.join(r)


def goal_check():
    return None


def main():
    return None

main()
print_board()
check_constraint(2)
