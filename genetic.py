"""
Genetic algorithm to solve nonogram
By Kayla Nguyen
"""
from nonogram import Nonogram
from solution import Solution
import random, operator


class GeneticAlgorithm(object):
    # instance of nonogram board
    global nonogram, population, fitness, ROWS, COLUMNS, ROW_COUNT, COLUMN_COUNT
    nonogram = Nonogram()
    population = []
    fitness = []

    ROWS = nonogram.get_row_constraints()
    COLUMNS = nonogram.get_column_constraints()
    ROW_COUNT = len(ROWS)
    COLUMN_COUNT = len(COLUMNS)

    # generate random population of suitable solutions for nonogram
    def generate_population(self):
        pop = []
        for i in range(0, 20):
            state = nonogram.get_random_state(ROWS, COLUMNS)
            # get solution generated based on row constraints
            pop.append(state[0])
        return pop

    # evaluate the fintness of each solution in the population
    def evaluate_fitness(self, pop):
        fit = []
        # print pop
        for sol in pop:
            fit.append(nonogram.check_all_col(sol))
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
            offspring = self.mutation(cross)
            # place new offspring in a new population
            pop.append(offspring)
        # return new generated population
        return pop

    # select 2 solutions from a population according to their fitness
    # the better fitness, the bigger chance to be selected
    def selection(self, pairs):
        sorted_pairs = sorted(pairs, key=operator.attrgetter('fitness'))
        sol1 = sorted_pairs[0]
        sol2 = sorted_pairs[1]

        '''print "chosen sol are"
        nonogram.print_state(sol1.get_state())
        print sol1.get_fit()
        nonogram.print_state(sol2.get_state())
        print sol2.get_fit()'''

        # list of 2 chosen solutions
        chosen = [sol1.get_state(), sol2.get_state()]
        return chosen

    # with a crossover probability cross over the parents to form a new offspring
    def crossover(self, parents):
        # generate a random crossover point
        crossover_point = random.randint(0, ROW_COUNT)

        # TODO
        # print ROW_COUNT
        # print crossover_point
        # nonogram.print_state(parents[0])

        # copy everything before this point from parent 1 and after this point from parent 2
        offspring = []
        for i in range(0, crossover_point):
            offspring.append(parents[0][i])
        for j in range(crossover_point, ROW_COUNT):
            offspring.append(parents[1][j])
        #TODO
        # nonogram.print_state(offspring)
        return offspring

    # with a mutation probability mutate new offspring at each locus (position in chromosome)
    def mutation(self, offspring):
        # new mutated offspring
        new = []
        for i in range(0, ROW_COUNT):
            # 10% chance a row get mutated
            probability = random.randint(0, 100)
            if probability <= 10:
                # print "row" + str(i) + " get mutated"
                # print offspring[i]
                rand = nonogram.get_random_row(i)
                # print "became"
                # print rand
                new.append(rand)

            else:
                new.append(offspring[i])
        return new

    # return solution if all constraints are met
    def check_goal(self, pop):
        for sol in pop:
            if nonogram.check_all_col(sol) is True:
                return sol
        return None

    # method to pair each solution with its fitness
    def pair_up(self, pop, fitness):
        pairs = []
        for i in range(0, len(pop)):
            solution = Solution(pop[i], fitness[i])
            pairs.append(solution)
        # TODO: Delete PRINT
        # nonogram.print_state(pairs[0].get_state())
        # print pairs[0].get_fit()
        return pairs

    # # method to check if a population has an optimal solution
    # def check_pop(self, pop):
    #     for sol in pop:
    #         nonogram.print_state(sol)
    #         if nonogram.goal_check(sol):
    #             return sol
    #     return None

    # main method
    def __init__(self):
        global population, fitness
        # STEP 1: generate random population
        population = self.generate_population()

        # loop to return the best solution in current population
        flag = None
        while flag is None:
            # STEP 2: evaluate fitness of each sol in population
            fitness = self.evaluate_fitness(population)
            # TODO: Print
            # print "fitness is"
            # print fitness
            # pair each solution with its fitness
            pairs = self.pair_up(population, fitness)

            # STEP 3: Create a new population
            population = self.create_new_population(pairs)
            # check if the end condition is satisfied
            flag = self.check_goal(population)

        print nonogram.print_state(flag)


GeneticAlgorithm()
