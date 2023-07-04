#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: main.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 8/5/2023
    brief: This file contains the main GP's program.
"""

import numpy as np
import trails_plots
from copy import deepcopy
from mutation import mutate
from multiprocessing import Process
from interpret import interpret_trail
from random import randint, choice, random
from classes import Instruction, Individual
from crossovers import one_point_crossover as crossover
from selection import tournament_selection as selection  # rewrite x in "import x as" to change a selection operator
from print_stats import print_stats_gen_avg_fitness, print_best_of_run, print_final_results
from init_params import (
    MAX_PROGRAM_LENGTH, MIN_PROGRAM_LENGTH, POP_SIZE,
    GRID_SIZE, MUTATION_RATE, POS_X, POS_Y, GENS,
    MAX_SUBROUTINES, MAX_SUBROUTINE_LENGTH, MIN_SUBROUTINE_LENGTH,
    XO_RATE, INSTRUCTION_LIST, SUBROUTINE_SYMBOLS,
    INIT_TYPE, INIT_PROGRAM_CONST, MAX_TIME, MAX_ANT_TRAIL_LEN
)


def verify_program():
    """
    Verify's the already generated solution. Just copy solution from the terminal into
    program.txt file and change generate_program() for verify_program() when initializing
    population.
    """

    ins = []
    program = Individual()

    with open('program.txt', 'r') as input_file:
        for line in input_file:
            ins.append(line.strip())
    
    for inst in ins:
        if 'IF FOOD_AHEAD ? ' in inst:
            instruction = Instruction(inst, fnc=True)
            program.insert_inst(instruction)
        elif '*' in inst:
            program.insert_inst(Instruction(inst, label=True))
        else:
            program.insert_inst(Instruction(inst))

    return program


def generate_program():
    """
    Creates a random program bound by program length requirements
    """

    program_length = None
    if INIT_TYPE == "RANGE": # initialization method, can be changed in init_params.py
        program_length = randint(MIN_PROGRAM_LENGTH, MAX_PROGRAM_LENGTH)
    elif INIT_TYPE == "MAX":
        program_length = MAX_PROGRAM_LENGTH
    elif INIT_TYPE == "MIN":
        program_length = MIN_PROGRAM_LENGTH
    elif INIT_TYPE == "CONST":
        program_length = INIT_PROGRAM_CONST

    program = Individual()

    # generate main program
    for _ in range(program_length):
        inst = choice(INSTRUCTION_LIST) # choose random instruction from a list

        if inst == "IF FOOD_AHEAD ? ": 
            # choose what happens when the ternary operator is executed
            true_opt = choice(SUBROUTINE_SYMBOLS[:MAX_SUBROUTINES] + INSTRUCTION_LIST[:-1])
            false_opt = choice(SUBROUTINE_SYMBOLS[:MAX_SUBROUTINES] + INSTRUCTION_LIST[:-1])

            # concatenate it
            inst = inst + true_opt + " : " + false_opt
            instruction = Instruction(inst, fnc=True)

        else:
            instruction = Instruction(inst)

        program.insert_inst(instruction)

    AV_SR_SYMB = SUBROUTINE_SYMBOLS[:MAX_SUBROUTINES] # set up letter-symbols for subroutines

    # generate soubroutines
    for _ in range(MAX_SUBROUTINES):
        symb = choice(AV_SR_SYMB)
        program.insert_inst(Instruction("* SR " + symb + ":", label=True, symb=symb))
        AV_SR_SYMB.pop(AV_SR_SYMB.index(symb)) # chosen symbol cannot be choseable again
        num_of_sr_ins = randint(MIN_SUBROUTINE_LENGTH, MAX_SUBROUTINE_LENGTH) # number of SR intrusctions
        for _ in range(num_of_sr_ins): # generate soubroutines program
            instruction = choice(INSTRUCTION_LIST[:-1])
            program.insert_inst(Instruction(instruction))

    return program


def liner_genetic_programming(change_params, params):
    """Main function of the LGP

    Args:
        change_params (int): whether parameters in params should be applicated
        params (array(int)): changable parameters (population size, crossover rate
                             and mutation rate) in case of running multiple runs 
                             of GP with different setting
    """
    global POP_SIZE, XO_RATE, MUTATION_RATE

    # changable parametrs during running multiple runs of the algorithm
    if change_params:
        POP_SIZE = params[0]
        XO_RATE = params[1]
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

    best_of_run = {
        "individual": None,
        "fitness": len(food_cells),
        "gen": 0,
        "best_of_run_path": None,
    }  
    
    gen_counter = [] # counts number of generations, used for stats
    trails_plots.plot_food_trail()

    # initializing ant's playing field
    grid = np.zeros((GRID_SIZE, GRID_SIZE)) # generates a 2D matrix
    grid_copy = deepcopy(grid)

    for food_cell in food_cells:
        grid[food_cell[POS_X]][food_cell[POS_Y]] = 1
        grid_copy[food_cell[POS_X]][food_cell[POS_Y]] = 1

    population = []
    # creating individual population
    for _ in range(POP_SIZE):
        program = generate_program()
        population.append(program)

    for individual in population:
        individual.reset_ant_info()
        grid = deepcopy(grid_copy)

        time = 0
        while time < MAX_TIME:
            if len(individual.trail) > MAX_ANT_TRAIL_LEN: break # terminating condition
            interpret_trail(individual, individual.ant, individual.trail, grid)

            time += 1

        for cell in individual.trail: # inserting indivudal's trail to grid
            grid[cell[POS_X]][cell[POS_Y]] = 2

        individual.count_fitness(grid)
        fitnesses['all_gen'].append(individual.fitness)

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

            if random() < XO_RATE: # crossover 
                parent1 = crossover(parent1, parent2)

            parent1 = mutate(parent1, MUTATION_RATE) # mutation 
            nextgen_population.append(parent1)
    
        population = nextgen_population
        fitnesses['all_gen'] = []

        # evaluatiing each individual
        for individual in population:
            individual.reset_ant_info()
            grid = deepcopy(grid_copy)

            time = 0
            while time < MAX_TIME:
                if len(individual.trail) > MAX_ANT_TRAIL_LEN: break
                
                interpret_trail(individual, individual.ant, individual.trail, grid)

                time += 1

            for cell in individual.trail: # inserting indivudal's trail to grid
                grid[cell[POS_X]][cell[POS_Y]] = 2

            individual.count_fitness(grid)
            fitnesses['all_gen'].append(individual.fitness)

        print_stats_gen_avg_fitness(gen, fitnesses['all_gen'])
        fitnesses['best_gen'].append(min(fitnesses['all_gen']))
        fitnesses['avg_gen'].append(np.round(np.average(fitnesses['all_gen'])))
        fitnesses['worst_gen'].append(max(fitnesses['all_gen']))

        for individual in population:
            if individual.fitness < best_of_run['fitness']:
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
        fns (array): array of geneticProgrammingAlg functions
        pop_size (int): population size
        cross_rate (int): crossover rate
        mut_rate (int): mutation rate
    """

    f = open("./results/results.txt", "a")
    f.write("\n")
    f.write("RUN. Algorithm Settings = POP_SIZE: " + str(pop_size) + ", CROSS_RATE: " + str(cross_rate)  + ", MUT_RATE: " + str(mut_rate) + " :: ")
    f.write("\n")
    f.close()

    print(" * LGP -- Linear Genetic Programming -- Langton's Ant Problem")

    parallel_computing(fns, params=True, change_params=[pop_size, cross_rate, mut_rate])


if __name__ == '__main__':

    NUM_OF_RUNS = 1 # number of desired runs which are going to be computed parallelly
    fns = [liner_genetic_programming for _ in range(NUM_OF_RUNS)]

    run_gp(fns, pop_size=100, cross_rate=0.7, mut_rate=1) 
