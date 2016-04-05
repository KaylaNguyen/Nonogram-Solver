"""
Genetic algorithm to solve nonogram
By Kayla Nguyen
"""


class GeneticAlgorithm(object):
    # generate random population of suitable solutions for nonogram
    def generate_population(self):
        pass

    # evaluate the fintness of each solution in the population
    def evaluate_fitness(self):
        pass

    # create a new population by repeating
    # selection, crossover, mutation, accepting
    def create_new_population(self):
        pass

    # select 2 solutions from a population according to their fitness
    # the better fitness, the bigger chance to be selected
    def selection(self):
        pass

    # with a crossover probability cross over the parents to form a new offspring
    def crossover(self):
        pass

    # with a mutation probability mutate new offspring at each locus (position in chromosome)
    def mutation(self):
        pass

    # place new offspring in a new population
    def accepting(self):
        pass

    # use new generated population instead of old one
    def replace(self):
        pass

    # if the end condition is satisfied, stop
    # and return the best solution in current population
    def test(self):
        pass

    # main method
    def main(self):
        pass
