"""
Solution/state class with fitness value
For genetic algorithm
By Kayla Nguyen
"""


class Solution(object):
    def __init__(self, given_state, given_fitness):
        self.state = given_state
        self.fitness = given_fitness

    def __cmp__(self, other):
        if self.fitness > other.fitness:
            return 1
        elif self.fitness < other.fitness:
            return -1
        else:
            return 0

    def get_state(self):
        return self.state

    def get_fit(self):
        return self.fitness