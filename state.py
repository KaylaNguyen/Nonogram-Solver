class State(object):
    """docstring for State"""

    def __init__(self, row_constraints, column_constraints):
        self.row_constraints = row_constraints
        self.column_constraints = column_constraints
        self.row_length = len(row_constraints) # y
        self.col_length = len(column_constraints) # x
        self.board = [["?" for x in range(self.col_length)] for y in range(self.row_length)]
        #print 'len(board): ', len(self.board)
        #print 'len(board[0]): ', len(self.board[0])
        #self.print_board()
        self.filledIndex = 0

    def get_board(self):
        return self.board

    def print_board(self):
        for i in self.board:
            print ' '.join(i)

    def add_row(self, row):
        self.board[self.filledIndex] = row
        self.filledIndex += 1

    def remove_row(self):
        if self.filledIndex == 0:
            return "Error: no row to remove"

        self.board[self.filledIndex - 1] = ["?"] * (self.row_length)
        self.filledIndex -= 1
    
    def to_string(self):
        s = ""
        for i in range(self.row_length):
            for j in self.board[i]:
                if j == '-':
                    s+= ' '
                else:
                    s += j 
                s += ' '
            #s+=' '.join(self.board[i])
            s+= '\n'
        return s

