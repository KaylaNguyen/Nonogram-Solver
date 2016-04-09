"""
Genetic algorithm to solve nonogram
By Kayla Nguyen
"""
from nonogram import Nonogram
import random


class GeneticAlgorithm(object):
    # instance of nonogram board
    global nonogram, population
    nonogram = Nonogram()
    population = []
    fitness = []

    # generate random population of suitable solutions for nonogram
    def generate_population(self):
        pop = []
        for i in range(0, 20):
            pop.append(nonogram.get_random_state(nonogram.ROWS, nonogram.COLUMNS))
        return pop

    # evaluate the fintness of each solution in the population
    def evaluate_fitness(self, pop):
        fit = []
        for sol in pop:
            fit.append(nonogram.check_constraint_col(sol))
        return fit

    # create a new population by repeating
    # selection, crossover, mutation, accepting
    def create_new_population(self, pairs):
        pop = []
        # create a new population by repeating
        # selection, crossover, mutation, accepting (placing new offspring in new pop)
        while len(pop) <= 20:
            parents = self.selection(pairs)
            cross = self.crossover(parents)
            offspring = self.mutation(offspring)
            # place new offspring in a new population
            pop.append(offspring)
        # return new generated population
        return pop

    # select 2 solutions from a population according to their fitness
    # the better fitness, the bigger chance to be selected
    def selection(self, pairs):
        sort_val = sorted(pairs.values())
        sol1 = sort_val[0]
        sol2 = sort_val[1]
        # list of 2 chosen solutions
        chosen = []
        for key, value in pairs:
            if len(chosen) <= 2:
                if value == sol1 or value == sol2:
                    chosen.append(key)
        return chosen

    # with a crossover probability cross over the parents to form a new offspring
    def crossover(self, parents):
        # generate a random crossover point
        crossover_point = random.randint(0, nonogram.ROW_COUNT - 1)
        # copy everything before this point from parent 1 and after this point from parent 2
        offspring = []
        for i in range(0, crossover_point):
            offspring.append(parents[0][i])
        for j in range(crossover_point, nonogram.ROW_COUNT):
            offspring.append(parents[1][j])
        return offspring

    # with a mutation probability mutate new offspring at each locus (position in chromosome)
    def mutation(self, offspring):
        # new mutated offspring
        new = []
        for i in range(0, nonogram.ROW_COUNT):
            probability = random.randint(0, 100)
            if probability <= 10:
                new.append(nonogram.get_random_row(i))
            else:
                new.append(offspring[i])
        return new

    # return solution if all constraints are met
    def check_goal(self, pop):
        for sol in pop:
            if nonogram.goal_check(sol) is True:
                return sol
            else:
                return None

    # main method
    def __init__(self):
        global population, fitness
        population = self.generate_population()
        # loop to return the best solution in current population
        flag = None
        while flag is None:
            fitness = self.evaluate_fitness(population)
            # pair each solution with its fitness
            pairs = dict(zip(population, fitness))
            # create new population
            population = self.create_new_population(pairs)
            # check if the end condition is satisfied
            flag = self.check_goal(population)

        print nonogram.print_state(flag)

GeneticAlgorithm()