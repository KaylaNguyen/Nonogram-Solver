''' CSP: Backtracking Search. Following pseudocode form textbook.'''
from nonogram import Nonogram
from state import State
from node import Node
import copy
#from time import sleep 

class Backtracking_Search():

    def __init__(self):
        self.nonogram = Nonogram()
        self.rows = self.nonogram.get_row_constraints()
        self.col = self.nonogram.get_column_constraints()
        self.row_length = len(self.rows)
        self.col_length = len(self.col)
        # define a state 
        self.state = State(self.rows, self.col)
        # get permutations from nonogram.py (attempt 1)
        self.col_permutations = self.hash_col_permutations()
        self.row_permutations = self.hash_row_permutations() 
        self.traversed = 0 
        self.all_created_nodes = 0 

    # Backtracking Search pseudocode from the textbook 
    # returns None if no solution is found 
    def backtracking_search(self, state):
        node = Node(state, None, 0)
        return self.recursive_backtracking(node)

    def recursive_backtracking(self, node):
        # check for goal state
        if self.is_goal(copy.deepcopy(node.state.get_board())):
            print 'Depth: ', node.depth 
            print 'All created nodes: ', self.all_created_nodes
            print 'All traversed: ', self.traversed
            return node
        
        # get al possible permutations for the row we're currently trying to fill
        rows = self.get_row_permutations(node.state.filledIndex)
        for row in rows:
            new_state = copy.deepcopy(node.state)
            new_state.add_row(list(row))
            self.all_created_nodes += 1
            
            # as long as this newly added row doesn't violate any constraints
            if self.check_violations(new_state):
                self.traversed += 1

                new_node = Node(new_state, node, node.depth + 1)
                result = self.recursive_backtracking(new_node)  # recurse
                if result is not None:
                    return result
                new_state.remove_row() # remove var from assignment 
        return None

    # Check constraint violation (2nd/successful attempt)
    def check_violations(self, state):
        if(state.filledIndex == len(state.get_board())): 
            if not self.is_goal(copy.deepcopy(state.get_board())): 
                return False 

        board = zip(*(state.get_board()))
        for i in range(0, len(board)): 
            if not self.check_col_violations(board[i], self.col[i]):
                return False 
        return True

    # check a single column 
    def check_col_violations(self, col, constraints):
        filled = 0 
        all_filled = 0 

        # check if there are too many '#' in the column; obviously a violation 
        for c in col: 
            if c == '#': 
                filled += 1
            if c != '?':
                all_filled += 1 

        if filled > sum(constraints):
            return False 

        counter = 0 # track block size
        curr_constraint = 0 # tracks the index of the constraint
        i = 0 
        while i < all_filled: 
            if curr_constraint == len(constraints): 
                break 
            if col[i] == '#': 
                if constraints[curr_constraint] > (all_filled - i):
                    return True 

                counter = 1 
                for j in range(i + 1, all_filled): 
                    if col[j] != '#':
                        break 
                    counter += 1 
                if counter != constraints[curr_constraint]: 
                    return False 
                curr_constraint += 1
                i += counter 
            else: 
                i += 1 
        return True 

    def is_goal(self, state):
        new_state = zip(*(state))
        for i in range(len(self.col_permutations)):
            if ''.join(new_state[i]) not in self.col_permutations[i]: 
                return False
        return True 

# -------------------- Previous Attempt(s) -----------------------
    def must_have_cols(self, col_constraints):
        # call must_have_rows and transpose the rows to columns
        return zip(*(self.must_have_rows(col_constraints)))

    # attempt 1
    def must_have_rows(self, row_constraints):
        solution = []

        for constraints in row_constraints:
            poss_sol = self.nonogram.get_permutations(constraints, len(row_constraints))
            row_sol = [True] * len(row_constraints)
            for sol in poss_sol:
                for i in range(len(sol)):
                    if sol[i] == '-':
                        row_sol[i] = False
            solution.append(row_sol)
        return solution

    # attempt 1 (unc)
    def constraint_check(self, board):
        solution = self.must_have_cols(self.col)
        for row in range(self.row_length):
            for col in range(self.col_length):
                # if the correct sol must have a "#" and it does not (ignore unfilled spots)
                # we've detected a constraint violation
                if solution[row][col] and board[row][col] == '-':
                    return False

        # other obvious checks
        for c in range(self.col_length):
            current_col = []
            for x in range(self.row_length):
                current_col.append(board[x][c])

            filled_count = 0
            for col in current_col:
                if col == '#':
                    filled_count += 1
            # check that there are not more filled blocks than constraints
            if filled_count > sum(self.col[c]):
                return False
            elif filled_count == sum(self.col[c]): # if filled == constraints, check goal
                # TODO: check if this function works?
                if self.nonogram.check_constraint_col(board, 0) != 0:
                    return False

        return True  # no constraint violations detected.

    # Takes the 'must have' row solutions and column solutions and figures out
    # which parts of the board absolutely must be filled ("#").
    # We probably won't need this because this is less restrictive than what we currently have
    # just for fun, not actually used anywhere. Might end up being useful tho.
    def get_all_constraints(self):
        row_sol = self.must_have_rows(self.rows)
        col_sol = self.must_have_cols(self.col)
        final_sol = [[False for x in range(self.row_length)] for y in range(self.col_length)]
        for i in range(self.col_length):
            for j in range(self.row_length):
                if row_sol[i][j] and col_sol[i][j]:
                    # if both are true
                    final_sol[i][j] = True
        return final_sol

    def hash_col_permutations(self): 
        # map index of column to a list of its constraints
        col = dict()
        for c in range(len(self.col)): 
            col[c] = self.nonogram.get_permutations(self.col[c], self.row_length)
        return col

    def hash_row_permutations(self):
        row = dict() 
        for r in range(len(self.rows)): 
            row[r] = self.nonogram.get_permutations(self.rows[r], self.col_length)
        return row 
   
    # returns the list of possible permutations at row[index]
    def get_row_permutations(self, index):
        return self.row_permutations[index]

    # returns the list of possible permutations at column[index]
    def get_col_permutations(self, index):
        return self.col_permutations[index]


main = Backtracking_Search()
goal_state = main.backtracking_search(main.state)
print "GOAL STATE: "
print goal_state.state.to_string() 
