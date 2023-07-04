#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: mutation.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 7/5/2023
    brief: this file contains mutate function(s) for evolving new population
"""

from random import random, choice
from classes import Instruction
from init_params import ( 
    MIN_PROGRAM_LENGTH,  MAX_PROGRAM_LENGTH, INSTRUCTION_LIST, 
    MAX_SUBROUTINE_LENGTH, MIN_SUBROUTINE_LENGTH, 
    MAX_SUBROUTINES, SUBROUTINE_SYMBOLS,
    MICROMUT_RATE, INSERTION_RATE,
    DELETION_RATE, MUTATION_RATE
    )


def mutate(individual, mut_rate):
    """ Function to mutate program. Goes inst. after inst. and checks probabilities of 
        inserting, deleting or mutating current inst. 

    Args:
        individual (list): a program to be mutated
    
    Return:
        individual (list): mutated program
    """

    global INSERTION_RATE, MUTATION_RATE, DELETION_RATE, MICROMUT_RATE
    if mut_rate != None:
        MUTATION_RATE, DELETION_RATE, INSERTION_RATE, MICROMUT_RATE = mut_rate, mut_rate, mut_rate, mut_rate

    MIN_LENGTH = MIN_PROGRAM_LENGTH
    MAX_LENGTH = MAX_PROGRAM_LENGTH
    inst_ord = 0

    # go through the entire main program n
    while inst_ord < individual.get_length_main_program():
        length = individual.get_length_main_program()

        # additive mutation
        if length < MAX_LENGTH and random() <= INSERTION_RATE:
            inst_name = choice(INSTRUCTION_LIST)
            inst = None

            # creating if food-ahead instruction
            if inst_name == 'IF FOOD_AHEAD ? ':
                # chose a subroutine symbol or instruction (obv. w/o the ternary operator)
                true_opt = choice(SUBROUTINE_SYMBOLS[:MAX_SUBROUTINES] + INSTRUCTION_LIST[:-1])
                false_opt = choice(SUBROUTINE_SYMBOLS[:MAX_SUBROUTINES] + INSTRUCTION_LIST[:-1])
                inst_name = inst_name + true_opt + " : " + false_opt
                inst = Instruction(inst_name, fnc=True)
            else:
                inst = Instruction(inst_name)
            individual.instructions.insert(inst_ord, inst)

        # destructive mutation
        elif length > MIN_LENGTH and random() <= DELETION_RATE:
            del individual.instructions[inst_ord]

        # mutation
        elif random() <= MUTATION_RATE:
            inst = choice(INSTRUCTION_LIST)

            # creating if food-ahead instruction
            if inst == 'IF FOOD_AHEAD ? ':
                true_opt = choice(SUBROUTINE_SYMBOLS[:MAX_SUBROUTINES] + INSTRUCTION_LIST[:-1])
                false_opt = choice(SUBROUTINE_SYMBOLS[:MAX_SUBROUTINES] + INSTRUCTION_LIST[:-1])
                inst = inst + true_opt + " : " + false_opt

            individual.instructions[inst_ord].set_inst(inst)

        # micromutation - can only happen withing if food-ahead instruciton
        elif "IF FOOD_AHEAD" in individual.instructions[inst_ord].data and random() <= MICROMUT_RATE:
            data = individual.instructions[inst_ord].data.split()
            data[3] = choice(SUBROUTINE_SYMBOLS[:MAX_SUBROUTINES] + INSTRUCTION_LIST[:-1])
            data[5] = choice(SUBROUTINE_SYMBOLS[:MAX_SUBROUTINES] + INSTRUCTION_LIST[:-1])
            data = ' '.join(data)
            individual.instructions[inst_ord].set_inst(data, fnc=True)

        inst_ord += 1

    MIN_LENGTH = MIN_SUBROUTINE_LENGTH
    MAX_LENGTH = MAX_SUBROUTINE_LENGTH

    # go through every subroutine
    for k in range(1, MAX_SUBROUTINES + 1):

        # get the position of first instruction in subroutine
        inst_ord = 0
        first_inst = individual.get_first_inst_subroutine(k) + 1

        # till you come across the another subroutine's label
        while first_inst + inst_ord < first_inst + individual.get_length_subroutine(k):
            
            current_length = individual.get_length_subroutine(k)

            # additive mutation
            if current_length < MAX_LENGTH and random() <= INSERTION_RATE:
                inst_name = choice(INSTRUCTION_LIST[0:2])
                inst = Instruction(inst_name)
                individual.instructions.insert(first_inst + inst_ord, inst)

            # destructive mutation
            elif current_length > MIN_LENGTH and random() <= DELETION_RATE:
                del individual.instructions[first_inst + inst_ord]

            # mutation    
            elif random() <= MUTATION_RATE:
                inst = choice(INSTRUCTION_LIST[0:2])
                individual.instructions[first_inst + inst_ord].set_inst(inst)

            # beacuse ternary operator is not allowed in subroutines, there is no need
            # for micromutation

            inst_ord += 1

    return individual