"""
Genetic algorithm to solve nonogram
Followed outline from www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php
By Kayla Nguyen
"""
from nonogram import Nonogram
from solution import Solution
import random, operator, time


class GeneticAlgorithm(object):
    global file
    file = open('output.txt', 'w')
    # instance of nonogram board
    global nonogram, population, fitness, ROWS, COLUMNS, ROW_COUNT, COLUMN_COUNT, POPSIZE, PROBABILITY
    nonogram = Nonogram()
    population = []
    fitness = []

    ROWS = nonogram.get_row_constraints()
    COLUMNS = nonogram.get_column_constraints()
    ROW_COUNT = len(ROWS)
    COLUMN_COUNT = len(COLUMNS)

    POPSIZE = 100
    PROBABILITY = 20

    # generate random population of suitable solutions for nonogram
    def generate_population(self):
        pop = []
        for i in range(0, POPSIZE):
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
        while len(pop) <= POPSIZE:
            parents = self.selection(pairs)
            cross = self.crossover(parents)
            offspring = self.mutation(cross)
            # place new offspring in a new population
            pop.append(offspring)
        '''WRITING TO FILE'''
        # file.write("PARENTS ARE\n")
        # file.write(nonogram.print_state(parents[0]))
        # file.write("\n")
        # file.write(nonogram.print_state(parents[1]))
        # file.write("\n")

        # return new generated population
        return pop

    # select 2 solutions from a population according to their fitness
    # the better fitness, the bigger chance to be selected
    def selection(self, pairs):
        sorted_pairs = sorted(pairs, key=operator.attrgetter('fitness'))
        sol1 = sorted_pairs[0]
        sol2 = sorted_pairs[1]

        # list of 2 chosen solutions
        chosen = [sol1.get_state(), sol2.get_state()]
        return chosen

    # with a crossover probability cross over the parents to form a new offspring
    def crossover(self, parents):
        # generate a random crossover point
        crossover_point = random.randint(0, ROW_COUNT)

        # copy everything before this point from parent 1 and after this point from parent 2
        offspring = []
        for i in range(0, crossover_point):
            offspring.append(parents[0][i])
        for j in range(crossover_point, ROW_COUNT):
            offspring.append(parents[1][j])
        return offspring

    # with a mutation probability mutate new offspring at each locus (position in chromosome)
    def mutation(self, offspring):
        # new mutated offspring
        new = []
        for i in range(0, ROW_COUNT):
            # 20% chance a row get mutated
            probability = random.randint(0, 100)
            if probability <= PROBABILITY:
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
            if nonogram.check_all_col(sol) is 0:
                return sol
        return None

    # method to pair each solution with its fitness
    def pair_up(self, pop, fitness):
        pairs = []
        for i in range(0, len(pop)):
            solution = Solution(pop[i], fitness[i])
            pairs.append(solution)
        return pairs

    # main method
    def __init__(self):
        start = time.time()

        global population, fitness
        # STEP 1: generate random population
        population = self.generate_population()

        # loop to return the best solution in current population
        flag = None
        counter = 0
        while flag is None:
            counter += 1
            string = "Generation " + str(counter) + "\n"
            file.write(string)
            # STEP 2: evaluate fitness of each sol in population
            fitness = self.evaluate_fitness(population)

            # pair each solution with its fitness
            pairs = self.pair_up(population, fitness)

            # STEP 3: create a new population
            population = self.create_new_population(pairs)

            # STEP 4: check if the end condition is satisfied
            flag = self.check_goal(population)
        end = time.time()
        runtime = end - start
        '''WRITING TO FILE'''
        # file.write("SOLUTION IS \n")
        # file.write(nonogram.print_state(flag))
        # file.write("\n")
        # file.write("\nRUNTIME IS")
        # file.write(str(runtime))
        print "RUNTIME IS %s" %runtime
        print "Number of generations: %s" % counter
        print (nonogram.print_state(flag))

'''
in selection
    choose 2 best sol into next gen
    then choose the rest by randomly choosing the sol with highest prob
    using roulette wheel
then crossover next gen
'''

GeneticAlgorithm()
