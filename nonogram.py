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


def check_constraint():
    return None


def print_board():
    for r in board:
        print ' '.join(r)


def goal_check():
    return None


def main():
    return None

main()
print_board()
