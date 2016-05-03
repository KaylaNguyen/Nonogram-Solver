"""
Genetic algorithm to solve nonogram
Followed outline from www.obitko.com/tutorials/genetic-algorithms/ga-basic-description.php
By Kayla Nguyen
"""
from nonogram import Nonogram
from solution import Solution
import random, operator, time, sys


class GeneticAlgorithm(object):
    global file
    file = open('output.txt', 'w')
    # instance of nonogram board
    global nonogram, population, fitness, ROWS, COLUMNS, ROW_COUNT, COLUMN_COUNT, POPSIZE, MUTATIONPROB, CROSSOVERPROB
    nonogram = Nonogram()
    population = []
    fitness = []

    ROWS = nonogram.get_row_constraints()
    COLUMNS = nonogram.get_column_constraints()
    ROW_COUNT = len(ROWS)
    COLUMN_COUNT = len(COLUMNS)

    POPSIZE = 300
    MUTATIONPROB = None
    CROSSOVERPROB = 75

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

    '''1ST APPROACH'''
    # create a new population by repeating
    # selection, crossover, mutation, accepting
    def create_new_population_1(self, pairs):
        pop = []
        # create a new population by repeating
        # selection, crossover, mutation, accepting (placing new offspring in new pop)
        parents = self.selection(pairs)
        while len(pop) <= POPSIZE:
            cross = self.crossover(parents)
            offspring = self.mutation(cross)
            # place new offspring in a new population
            pop.append(offspring)

        print ("PARENTS ARE\n")
        print nonogram.print_state(parents[0])
        print("\n\n")
        print nonogram.print_state(parents[1])
        print("\n\n")

        # return new generated population
        return pop

    '''2ND APPROACH'''
    # create a new population by repeating
    # selection, crossover, mutation, accepting
    def create_new_population_2(self, pairs):
        pre_pop = []
        # create a new population by repeating
        # selection, crossover, mutation, accepting (placing new offspring in new pop)

        # select best individuals based on their fitness
        chosen = self.selection_2(pairs)
        chosen = sorted(chosen, key=operator.attrgetter('fitness'))
        pre_pop.append(chosen[0].get_state())
        pre_pop.append(chosen[1].get_state())
        # the rest crossover
        cross = self.crossover_2(chosen[2:])
        pre_pop.extend(cross)

        # print pre_pop

        # mutate the whole pre_pop
        post_pop = []
        for i in range(0, len(pre_pop)):
            offspring = self.mutation(pre_pop[i])
            # place new offspring in a new population
            post_pop.append(offspring)

        # '''WRITING TO FILE'''
        # file.write("BEST 2 ARE\n")
        # file.write(nonogram.print_state(chosen[0].get_state()))
        # file.write(str(chosen[0].get_fit()))
        # file.write("\n\n")
        # file.write(nonogram.print_state(chosen[1].get_state()))
        # file.write(str(chosen[1].get_fit()))
        # file.write("\n\n")

        print ("BEST 2 ARE\n")
        print nonogram.print_state(chosen[0].get_state())
        print str(chosen[0].get_fit())
        print("\n\n")
        print nonogram.print_state(chosen[1].get_state())
        print(str(chosen[1].get_fit()))
        print("\n\n")

        # return new generated population
        return post_pop

    # use roulette wheel to select best solutions from a population according to their fitness
    # the better fitness, the bigger chance to be selected
    def selection_2(self, pairs):
        sum_fit = 0
        # store fitness in an array
        fit_array = []
        for i in pairs:
            sum_fit += i.get_fit()
            fit_array.append(i.get_fit())
        # print "sum fit is", sum_fit
        fit_array.reverse()

        chosen = []
        fitness_function = []
        index = 0
        for j in fit_array:
            fit_val = j
            # print "fit val is", fit_val
            fitness_function.append(range(index, index + fit_val))
            index += fit_val
        # print fitness_function

        for k in range(0, POPSIZE):
            probability = random.randint(0, sum_fit)
            for a in range(0, len(fitness_function)):
                if probability in fitness_function[a]:
                    chosen.append(pairs[a])
        # print len(chosen)
        # print chosen
        return chosen

    # with a crossover probability cross over the parents to form 2 new offsprings
    # return a list of new offsprings
    def crossover_2(self, parents):
        index_i = 0
        index_j = 1
        # list of offsprings to return
        list = []
        while index_i < len(parents) and index_j < len(parents):
            # generate a random probability
            probability = random.randint(0, 100)
            if probability < CROSSOVERPROB:
                # generate a random crossover point
                crossover_point = random.randint(0, ROW_COUNT)
                # copy everything before this point from parent 1 and after this point from parent 2
                offspring1 = []
                offspring2 = []
                # get states of parents
                state1 = parents[index_i].get_state()
                state2 = parents[index_j].get_state()

                for i in range(0, crossover_point):
                    offspring1.append(state1[i])
                    offspring2.append(state2[i])
                for j in range(crossover_point, ROW_COUNT):
                    offspring1.append(state2[j])
                    offspring2.append(state1[j])
                list.append(offspring1)
                list.append(offspring2)
            else:
                list.append(parents[index_i].get_state())
                list.append(parents[index_j].get_state())
            index_i += 2
            index_j += 2
        return list

    '''1ST APPROACH'''
    # select 2 solutions from a population according to their fitness
    # the better fitness, the bigger chance to be selected
    def selection(self, pairs):
        sorted_pairs = sorted(pairs, key=operator.attrgetter('fitness'))
        sol1 = sorted_pairs[0]
        sol2 = sorted_pairs[1]

        # '''WRITING TO FILE'''
        # file.write("PARENTS ARE\n")
        # file.write(nonogram.print_state(sol1.get_state()))
        # file.write(str(sol1.get_fit()))
        # file.write("\n")
        # file.write(nonogram.print_state(sol2.get_state()))
        # file.write(str(sol2.get_fit()))
        # file.write("\n")

        # list of 2 chosen solutions
        chosen = [sol1.get_state(), sol2.get_state()]
        return chosen

    # with a crossover probability cross over the parents to form a new offspring
    def crossover(self, parents):
        # generate a random probability
        probability = random.randint(0, 100)
        if probability < CROSSOVERPROB:
            # generate a random crossover point
            crossover_point = random.randint(0, ROW_COUNT)

            # copy everything before this point from parent 1 and after this point from parent 2
            offspring = []
            for i in range(0, crossover_point):
                offspring.append(parents[0][i])
            for j in range(crossover_point, ROW_COUNT):
                offspring.append(parents[1][j])
        else:
            offspring = parents[0]
        return offspring

    # with a mutation probability mutate new offspring at each locus (position in chromosome)
    def mutation(self, offspring):
        # new mutated offspring
        new = []
        for i in range(0, ROW_COUNT):
            # 20% chance a row get mutated
            probability = random.randint(0, 100)
            if probability <= MUTATIONPROB:
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
        if len(sys.argv) == 1:
            print "Choose an approach: greedy or proper"
            print "'python genetic.py greedy' or 'python genetic.py proper'"
            return

        if str(sys.argv[1]) == "greedy":
            global MUTATIONPROB
            MUTATIONPROB = 30

        elif str(sys.argv[1]) == "proper":
            global MUTATIONPROB
            MUTATIONPROB = 5

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
            # file.write(string)
            # STEP 2: evaluate fitness of each sol in population
            fitness = self.evaluate_fitness(population)

            # pair each solution with its fitness
            pairs = self.pair_up(population, fitness)

            # STEP 3: create a new population

            if str(sys.argv[1]) == "greedy":
                population = self.create_new_population_1(pairs)
            elif str(sys.argv[1]) == "proper":
                population = self.create_new_population_2(pairs)

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

GeneticAlgorithm()
