#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: main.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 21/4/2023
    brief: This file contains main function for Genetic Programming, function for verifying specific soluton,
           and ability to run multiple instances of this algorithm in the same time.
"""

import numpy as np
import trails_plots
from tree import GPTree
from copy import deepcopy
from random import random, randint
from multiprocessing import Process
from interpret import interpret_trail
from selection import tournament_selection as selection
from crossovers import crossover_twice_mutation, crossover_and_cut
from print_stats import print_stats_gen_avg_fitness, print_best_of_run, print_final_results
from init_params import (POP_SIZE, MIN_DEPTH, GENS, CROSSOVER_RATE, GRID_SIZE, MUTATION_RATE,
                          MAX_DEPTH, MAX_TIME, POS_X, POS_Y, GRID, MAX_ANT_TRAIL_LEN)


def verify_program(pos, tree):
    """
    Verify's the already generated solution. Just copy solution from the terminal into
    program.txt file and change generate_program() for verify_program() when initializing
    population. Disclaimer - still does not work properly.
    """

    ins = [] # vertices
    with open('program.txt', 'r') as input_file:
        for line in input_file:
            ins.append(line.strip())
    
    data = ins[pos]
    del ins[pos]
    tree.data = data
    tree.print_tree()

    if data in ('PROGN2', 'IF_FOOD_AHEAD', 'PROGN3'):

        tree.left = GPTree()
        verify_program(pos, tree.left)
        if data == 'PROGN3':

            tree.middle = GPTree()
            verify_program(pos, tree.middle)

        tree.right = GPTree()
        verify_program(pos, tree.right)
    
    return tree


def init_population(): 
    """Function to initialize first population, either using grow or full method
        Modified function from the author (Moshe Sipper) of tiny_gp. See tree.py for more.
    Returns:
        array: population of candidate solutions
    """
    pop = [] # population
    for _ in range(POP_SIZE): # generate as many indiviuals as is the number of POP_SIZE 
        md = randint(MIN_DEPTH, MAX_DEPTH) # randomly choose maximum depth of the following individual
        depth = 0
        while depth < MIN_DEPTH: # checks if the individual fulfills the minimals size in case of using grow method
            t = GPTree()
            t.random_tree(grow=True, max_depth=md) # grow == True => GROW, otherwise FULL method
            depth = t.height()
        pop.append(t)
          
    return pop
  

def tree_genetic_programming(change_params, params):
    """Main function of the TGP

    Args:
        change_params (int): whether parameters in params should be applicated
        params (array(int)): changable parameters (population size, crossover rate
                             and mutation rate) in case of running multiple runs 
                             of GP with different setting
    """
    global POP_SIZE, CROSSOVER_RATE, MUTATION_RATE

    # changable parametrs during running multiple runs of the algorithm
    if change_params:
        POP_SIZE = params[0]
        CROSSOVER_RATE = params[1]
        MUTATION_RATE = params[2]
    
    # independent of the population, so that the equation 
    # 'population size * generation = constant'is always true
    GENS = 10000 // POP_SIZE # if wanna use number from init_params, just comment this line

    food_cells = trails_plots.trail_santafe_32x32 # selected trail
    
    fitnesses = {
        'all_gen': [], # fitnesses of each individual at each generation
        'best': [], # best fitnesses without duplicates
        'best_gen': [], # best individual at each generation 
        'avg_gen': [], # average fitness at each generation
        'worst_gen': [] # worst individual at each generation
    }

    # dictionary holding the fittest individual of the run
    best_of_run = {
        'individual': None,
        'fitness': len(food_cells),
        'gen': 0,
        'best_of_run_path': 0
    }

    gen_counter = [] # counts number of generations, used for stats

    grid = np.zeros((GRID_SIZE, GRID_SIZE)) # generates a 2D matrix
    grid_copy = deepcopy(grid)

    # filling the grid with ones which represent where the food is present
    for cell in food_cells:
        grid[cell[POS_X]][cell[POS_Y]] = 1
        grid_copy[cell[POS_X]][cell[POS_Y]] = 1

    population = init_population() # initialiaze starting population
    trails_plots.plot_food_trail()

    # initial rating of each individual
    for individual in population:
        individual.reset_ant_info()
        grid = deepcopy(grid_copy)

        time = 0
        while time < MAX_TIME:
            if len(individual.trail) > MAX_ANT_TRAIL_LEN: break # terminating condition

            interpret_trail(individual, individual.ant, individual.trail, grid)

            time += 1

        # filling the grid with twos, which represent ant's trail so far
        for cell in individual.trail:
            grid[cell[POS_X]][cell[POS_Y]] = 2

        individual.count_fitness(grid)
        fitnesses['all_gen'].append(individual.fitness)
    
    # let the evolution begin!
    for gen in range(GENS):
        nextgen_population = []

        # securing that the best individual proceeds to the next generation
        elite_individual = population[0]
        for individual in population:
            if individual.fitness < elite_individual.fitness:
                elite_individual = individual
        nextgen_population.append(deepcopy(elite_individual))


        # -1, because elite individual is already in next generation    
        for _ in range(POP_SIZE - 1): 
            parent1 = selection(population) # selecting two parents for evolution
            parent2 = selection(population)

            if random() < CROSSOVER_RATE: # crossover
                parent1 = crossover_and_cut(parent1, parent2)

            if random() < MUTATION_RATE: # mutation
                parent1.mutation([randint(0, parent1.size())])
                if parent1.height() > MAX_DEPTH:
                    parent1.align_tree()

            nextgen_population.append(parent1)

        population = nextgen_population
        fitnesses['all_gen'] = []

        # evaluatiing each individual
        for individual in population:
            individual.reset_ant_info()
            grid = deepcopy(grid_copy)

            time = 0
            while time < MAX_TIME:
                if len(individual.trail) > MAX_ANT_TRAIL_LEN: break # terminanting condition
                
                interpret_trail(individual, individual.ant, individual.trail, grid)

                time += 1

            # filling the grid with twos, which represent ant's trail so far
            for cell in individual.trail:
                grid[cell[POS_X]][cell[POS_Y]] = 2

            individual.count_fitness(grid)
            fitnesses['all_gen'].append(individual.fitness)

        print_stats_gen_avg_fitness(gen, fitnesses['all_gen'])

        fitnesses['best_gen'].append(min(fitnesses['all_gen']))
        fitnesses['avg_gen'].append(np.round(np.average(fitnesses['all_gen']), 2))
        fitnesses['worst_gen'].append(max(fitnesses['all_gen']))

        # searching if there is any better individual
        # if so, set it as the best_of_Run
        for individual in population:
            if individual.fitness <  best_of_run['fitness']:

                best_of_run['fitness'] = deepcopy(individual.fitness)
                best_of_run['gen'] = gen
                best_of_run['path'] = deepcopy(individual.trail)
                best_of_run['individual'] = deepcopy(individual)

                print_best_of_run(best_of_run)
                fitnesses['best'].append(best_of_run['fitness'])
                
        gen_counter.append(gen)

        if best_of_run['fitness'] == 0: # terminating condition
            break
        
    print_final_results(fitnesses, best_of_run)
   

def parallel_computing(fns, params, change_params):
    """Function which runs GP mutilple times using multithreading.

    Args:
        fns (array): array of geneticProgrammingAlg functions
        params (bool): when True, change params are applied, otherwise not (False)
        change_params (array): array of three main parameters (POP_SIZE, CROSSOVER_RATE, MUTATION_RATE)
    """

    proc = [] # processes
    for function in fns:
        p = Process(target=function, args=(params, change_params))
        p.start()
        proc.append(p)
    for process in proc:
        process.join()


def run_gp(fns, pop_size, cross_rate, mut_rate):
    """Function prints settings of algorithm to results.txt file and starts parellel computing

    Args:
        fns (array): array of tree_genetic_programming functions
        pop_size (int): population size
        cross_rate (int): crossover rate
        mut_rate (int): mutation rate
    """

    f = open("./results/results.txt", "a")
    f.write("\n")
    f.write("RUN. Algorithm Settings = POP_SIZE: " + str(pop_size) + ", CROSS_RATE: " + str(cross_rate)  + ", MUT_RATE: " + str(mut_rate) + " :: ")
    f.write("\n")
    f.close()

    parallel_computing(fns, params=True, change_params=[pop_size, cross_rate, mut_rate])


if __name__ == '__main__':

    NUM_OF_RUNS = 1 # number of desired runs which are going to be computed parallelly
    fns = [tree_genetic_programming for _ in range(NUM_OF_RUNS)]

    run_gp(fns, pop_size=100, cross_rate=1, mut_rate=1) # runs NUM_OF_RUNS parallel
