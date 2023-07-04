#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    file: crossovers.py
    author: Tadeáš Kachyňa, <xkachy00@fit.vutbr.cz>
    date: 8/5/2023
    brief: This file contains crossover function(s) for evolving new population. These two variants
        (one-point and two-point crossovers) work analogously, as they are described in the theoretical 
        and practical part of the bachelor thesis.
"""
from random import randint
from classes import Individual
from copy import deepcopy
from init_params import MAX_PROGRAM_LENGTH, MAX_SUBROUTINES, MIN_PROGRAM_LENGTH


def subroutines_crossover(individual_1, individual_2, new_individual_1, new_individual_2):
    first_sr = randint(1, MAX_SUBROUTINES)
    second_sr = randint(1, MAX_SUBROUTINES)

    # get the position of both subroutines in old and new phenotypes
    first_sr_pos = new_individual_1.get_first_inst_subroutine(first_sr)
    second_sr_pos = new_individual_2.get_first_inst_subroutine(second_sr)
    first_sr_pos_old = individual_1.get_first_inst_subroutine(first_sr)
    second_sr_pos_old = individual_2.get_first_inst_subroutine(second_sr)

    # delete subroutines in new individuals
    pos = first_sr_pos
    while not new_individual_1.instructions[pos+1].label:
        del new_individual_1.instructions[pos+1]
        if new_individual_1.instructions[pos] == new_individual_1.instructions[-1]:
            break

    pos = second_sr_pos
    while not new_individual_2.instructions[pos+1].label:
        del new_individual_2.instructions[pos+1]
        if new_individual_2.instructions[pos] == new_individual_2.instructions[-1]:
            break

    # insert subroutines into new individuals
    while not individual_2.instructions[second_sr_pos_old+1].label:
        new_individual_1.instructions.insert(first_sr_pos+1,deepcopy(individual_2.instructions[second_sr_pos_old+1]))
        second_sr_pos_old += 1
        first_sr_pos += 1
        if individual_2.instructions[second_sr_pos_old] == individual_2.instructions[-1]:
            break

    while not individual_1.instructions[first_sr_pos_old+1].label:
        new_individual_2.instructions.insert(second_sr_pos+1,deepcopy(individual_1.instructions[first_sr_pos_old+1]))
        first_sr_pos_old += 1
        second_sr_pos += 1
        if individual_1.instructions[first_sr_pos_old] == individual_1.instructions[-1]:
            break

    return new_individual_1, new_individual_2

def one_point_crossover(individual_1, individual_2):
    """Simple one-point crossovers where last two segments replace each other 
    both parents. Randomly selected subroutine from each parents will also change
    their place.

    Args:
        individual_1 (Individual): first parent
        individual_2 (Individual): second parent

    Returns:
        Individual: new offspring
    """

    # randomly choose crossover point in each parent
    crossover_point_1 = randint(1, individual_1.get_length_main_program())
    crossover_point_2 = randint(1, individual_2.get_length_main_program())

    # create new offsprings
    new_individual_1 = Individual()
    new_individual_2 = Individual()    

    # -- MAIN PROGRAM CROSSOVER --#
    # copy the first part of the first parent to the new individual
    inst_ord = 0
    while inst_ord < crossover_point_1:
        new_individual_1.instructions.append(deepcopy(individual_1.instructions[inst_ord]))
        inst_ord += 1

    # copy the first part of the second parent to the new individual
    inst_ord = 0
    while inst_ord < crossover_point_2:
        new_individual_2.instructions.append(deepcopy(individual_2.instructions[inst_ord]))
        inst_ord += 1

    # copy the second part of the first parent to the second new individual
    inst_ord = crossover_point_1
    while inst_ord < individual_1.get_length():
        new_individual_2.instructions.append(deepcopy(individual_1.instructions[inst_ord]))
        inst_ord += 1

    # copy the second part of the second part to the first new individual
    inst_ord = crossover_point_2
    while inst_ord < individual_2.get_length():
        new_individual_1.instructions.append(deepcopy(individual_2.instructions[inst_ord]))
        inst_ord += 1

    # check whether the new offspring fits in the limit size or not
    if new_individual_1.get_length_main_program() > MAX_PROGRAM_LENGTH:
       length = new_individual_1.get_length_main_program()
       # if not, align it to the max length
       del new_individual_1.instructions[MAX_PROGRAM_LENGTH:length]
    
    # to the same for the second offspring
    if new_individual_2.get_length_main_program() > MAX_PROGRAM_LENGTH:
       length = new_individual_2.get_length_main_program()
       del new_individual_2.instructions[MAX_PROGRAM_LENGTH:length]

    # -- SUBROUTINES CROSSOVER -- #
    # selecting subroutines to exchange
    new_individual_1, new_individual_2 = subroutines_crossover(individual_1, individual_2, 
                                                               new_individual_1, new_individual_2)

    # return only one individual
    if new_individual_1.get_length_main_program() > MIN_PROGRAM_LENGTH:
        return new_individual_1
    else:
        return new_individual_2


def two_point_crossover(individual_1, individual_2):
    """Simple two-point crossovers where the midle segments replace each other 
    both parents. Randomly selected subroutine from each parents will also change
    their place.

    Args:
        individual_1 (Individual): first parent
        individual_2 (Individual): second parent

    Returns:
        Individual: new offspring
    """

    # get the length of main programs of each parent
    length_mp_ind1 = individual_1.get_length_main_program()
    length_mp_ind2 = individual_2.get_length_main_program()

    # randomly choose crossover points from each parent
    crossover_point_1 = randint(1, individual_1.get_length_main_program()//2)
    crossover_point_2 = randint(1, individual_2.get_length_main_program()//2)

    # choose the length of the middle segment
    segment_ind1 = randint(crossover_point_1, length_mp_ind1 - 1)
    segment_ind2 = randint(crossover_point_2, length_mp_ind2 - 1)

    # create offsprings
    new_individual_1 = Individual()
    new_individual_2 = Individual()   

    # copy the left segment from the first parent to the first new individual
    inst_ord = 0
    while inst_ord < crossover_point_1:
        new_individual_1.instructions.append(deepcopy(individual_1.instructions[inst_ord]))
        inst_ord += 1

    # copy the left segment from the second parent to the second new individual
    inst_ord = 0
    while inst_ord < crossover_point_2:
        new_individual_2.instructions.append(deepcopy(individual_2.instructions[inst_ord]))
        inst_ord += 1

    # copy the middle segment from the first parent to the second new individual
    inst_ord = crossover_point_1
    while inst_ord < segment_ind1:
        new_individual_2.instructions.append(deepcopy(individual_1.instructions[inst_ord]))
        inst_ord += 1

    # copy the middle segment from the second parent to the first new individual
    inst_ord = crossover_point_2
    while inst_ord < segment_ind2:
        new_individual_1.instructions.append(deepcopy(individual_2.instructions[inst_ord]))
        inst_ord += 1
    
    # copy the right segment from the first parent to the first new individual
    inst_ord = segment_ind1
    while inst_ord < individual_1.get_length():
        new_individual_1.instructions.append(deepcopy(individual_1.instructions[inst_ord]))
        inst_ord += 1

     # copy the right segment from the second parent to the second new individual
    inst_ord = segment_ind2
    while inst_ord < individual_2.get_length():
        new_individual_2.instructions.append(deepcopy(individual_2.instructions[inst_ord]))
        inst_ord += 1

    # check whether the new offspring fits in the limit size or not
    if new_individual_1.get_length_main_program() > MAX_PROGRAM_LENGTH:
       length = new_individual_1.get_length_main_program()
       # if not, align it to the max length
       del new_individual_1.instructions[MAX_PROGRAM_LENGTH:length]
    
    # to the same for the second offspring
    if new_individual_2.get_length_main_program() > MAX_PROGRAM_LENGTH:
       length = new_individual_2.get_length_main_program()
       del new_individual_2.instructions[MAX_PROGRAM_LENGTH:length]

    # -- SUBROUTINES CROSSOVER -- #
    # selecting subroutines to exchange
    new_individual_1, new_individual_2 = subroutines_crossover(individual_1, individual_2, 
                                                               new_individual_1, new_individual_2)

    # return only one individual
    if new_individual_1.get_length_main_program() > MIN_PROGRAM_LENGTH:
        return new_individual_1
    else:
        return new_individual_2
