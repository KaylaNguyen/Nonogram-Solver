# Nonogram/Griddler solver
# Matthew Strawbridge
# November 2009
# --
# Creative Commons Attribution 2.0 UK: England & Wales
# http://creativecommons.org/licenses/by/2.0/uk/

# Define some character constants
BLANK = " "
FILL = "#"
UNKNOWN = "?"

# Example data taken from The Sunday Telegraph, 2009-11-01
ROWS = [[2, 2], [7], [2, 4], [7], [5], [3], [1]]

COLUMNS = [[3], [5], [2, 3], [6], [6], [5], [3]]

ROW_COUNT = len(ROWS)
COLUMN_COUNT = len(COLUMNS)


def min_width(blocks):
    """The minimum width into which the supplied blocks will fit

    e.g. min_width([1,2,3]) = 8
    """
    assert (len(blocks) > 0)
    return sum(blocks) + len(blocks) - 1


def fit(blocks, size):
    """Return all possible ways of fitting the supplied blocks into the
    supplied size.
    """
    assert (len(blocks) > 0)
    assert (size >= min_width(blocks))
    if len(blocks) == 1:
        return [BLANK * i + FILL * blocks[0] + BLANK * (size - blocks[0] - i)
                for i in range(size - blocks[0] + 1)]
    else:
        return [BLANK * (i - blocks[0]) + FILL * blocks[0] + BLANK + f2
                for i in range(blocks[0], size - min_width(blocks[1:]))
                for f2 in fit(blocks[1:], size - i - 1)]


def solve_row(candidates):
    """Return a string formed by merging the candidate solutions.

    At each position the character will be FILL if all candidates have
    FILL in that position, BLANK if they all have BLANK or UNKNOWN
    if there is a mixture.
    """
    return [UNKNOWN if len(x) > 1
            else x.pop()
            for x in [set(y) for y in transpose(candidates)]]


def matches(candidate, pattern):
    """Returns True if the candidate matches the pattern, False otherwise."""
    assert (len(candidate) == len(pattern))
    for i in range(len(pattern)):
        if pattern[i] != UNKNOWN and pattern[i] != candidate[i]:
            return False
    return True


def print_grid(g):
    """Print out the grid (an array of arrays of characters)."""
    for row in g:
        print ''.join(row)


def transpose(g):
    """Returns the transposed version of the supplied matrix
    (i.e. rows become columns and columns become rows).
    """
    assert g
    return map(lambda *row: list(row), *g)


def is_solved(candidate):
    """Returns True if the supplied candidate is a complete solution
    (contains no UNKNOWN entries), False otherwise.
    """
    return reduce(lambda x, y: x and not UNKNOWN in y, candidate, True)


def update_solution(grid, row, pattern):
    """Update the specified row of the grid from the pattern, overwriting
    any non-UNKNOWN values from the pattern.
    """
    for p in range(len(pattern)):
        if pattern[p] != UNKNOWN:
            grid[row][p] = pattern[p]


def main():
    # Initially fill the solution with a grid of UNKNOWNs
    solution = [[UNKNOWN for x in range(COLUMN_COUNT)]
                for y in range(ROW_COUNT)]

    # Generate all possible fits for the rows and columns
    fits_r = [fit(row, COLUMN_COUNT) for row in ROWS]
    fits_c = [fit(col, ROW_COUNT) for col in COLUMNS]
    fits = [fits_r, fits_c]
    row_col = 0  # current index into fits; 0 = row, 1 = column

    while not is_solved(solution):
        assert (row_col == 0 or row_col == 1)
        # Filter out any impossible fits given the solution so far
        for ri in range(len(fits[row_col])):
            fits[row_col][ri] = filter(lambda x: matches(x, solution[ri]),
                                       fits[row_col][ri])
            this_solution = solve_row(fits[row_col][ri])
            update_solution(solution, ri, this_solution)
        row_col = abs(row_col - 1)  # toggle 0, 1
        solution = transpose(solution)

    if row_col == 0:
        transpose(solution)

    print_grid(solution)


main()
