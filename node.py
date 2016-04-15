class Node(object):
    """A node points to a state, the previous node in the search tree and the current depth"""

    def __init__(self, state, prev_node, depth):
        self.state = state
        self.parent = prev_node
        self.depth = depth
