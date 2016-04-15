from nonogram import Nonogram
from state import State
from node import Node
import copy 

class Backtracking_Search(object):
	"""docstring for Backtracking_Search"""
	def __init__(self):
		self.nonogram = Nonogram() 
		self.rows = self.nonogram.get_rows()
		self.col = self.nonogram.get_cols()
		self.row_length = len(self.rows)
		self.col_length = len(self.col)
		self.state = State(self.rows, self.col) 

	# pass in an initial state 
	def backtracking_search(self, state):
		node = Node(state, None, 0)
		return self.recursive_backtracking(node) 

	def recursive_backtracking(self, node):
		# check for goal state 
		if self.nonogram.goal_check(copy.deepcopy(node.state.get_board())):
			return node 
		# get all possible permutations for the row we're currently trying to fill 
		rows = self.nonogram.get_permutations(self.rows[node.state.filledIndex], len(self.rows))
		new_state = copy.deepcopy(node.state)
		for row in rows: 
			new_state.add_row(list(row))
			# as long as this newly added row doesn't violate any constraints
			if self.constraint_check(new_state.get_board()): 
				new_node = Node(new_state, node, node.depth + 1)
				result = self.recursive_backtracking(new_node) # recurse 
				if result is not None: 
					return result 
			new_state.remove_row() 
		return None 

	def must_have_rows(self, row_constraints):
		solution = [] 

		for constraints in row_constraints:
			poss_sol = self.nonogram.get_permutations(constraints, len(row_constraints))
			row_sol = [True]*len(row_constraints)
			for sol in poss_sol:
				for i in range(len(sol)):
					if sol[i] == '-':
						row_sol[i] = False 
			solution.append(row_sol)
		return solution 

	def must_have_cols(self, col_constraints):
		# call must_have_rows and transpose the rows to columns 
		return zip(*(self.must_have_rows(col_constraints)))

	def constraint_check(self, board):
		solution = self.must_have_cols(self.col)
		for row in range(self.row_length): 
			for col in range(self.col_length):
				# if the correct sol must have a "#" and it does not (ignore unfilled spots)
				# we've detected a constraint violation  
				if solution[row][col] and board[row][col] == '-':
					return False 

		# other bullshit checks 
		for c in range(self.col_length):
			current_col = [] 
			for x in range(self.row_length):
				current_col.append(board[x][c])

			filled_count = 0 
			for col in current_col: 
				if col == '#':
					filled_count += 1

			if filled_count > sum(self.col[c]):
				return False
			elif filled_count == sum(self.col[c]):
				# TODO: check if this function works? 
				if self.nonogram.check_constraint_col(board, 0) != 0: 
					return False 

		return True # no constraint violations detected. 

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
		


main = Backtracking_Search()

goal_state = main.backtracking_search(main.state)
for row in goal_state.state.get_board():
	print ' '.join(row)






		