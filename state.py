class State(object):
    """docstring for State"""

    def __init__(self, row_constraints, column_constraints):
        self.row_constraints = row_constraints
        self.column_constraints = column_constraints
        self.row_length = len(row_constraints)
        self.col_length = len(column_constraints)
        self.board = [["?" for x in range(self.row_length)] for y in range(self.col_length)]
        self.filledIndex = 0

    def get_board(self):
        return self.board

    def print_board(self):
        for i in self.board:
            print i

    def add_row(self, row):
        self.board[self.filledIndex] = row
        self.filledIndex += 1

    def remove_row(self):
        if self.filledIndex == 0:
            return "Error: no row to remove"

        self.board[self.filledIndex - 1] = ["?"] * (self.row_length)
        self.filledIndex -= 1
